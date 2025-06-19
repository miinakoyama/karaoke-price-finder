"use client"

import { useState } from "react"
import { SearchPage } from "./pages/SearchPage"
import { ResultsPage } from "./pages/ResultsPage"
import { StoreDetail } from "./pages/StoreDetail"
import { Store, MembershipSettings, PlanDetail, mockStores } from "./types/store"

export default function KaraokeSearchApp() {
  const [currentView, setCurrentView] = useState<"home" | "results">("home")
  const [viewMode, setViewMode] = useState<"list" | "map">("list")
  const [selectedStore, setSelectedStore] = useState<Store | null>(null)
  const [stores, setStores] = useState<Store[]>([])
  const [searchLocation, setSearchLocation] = useState("")
  const [coords, setCoords] = useState<{ lat: number | null; lng: number | null }>({ lat: null, lng: null })
  const [distance, setDistance] = useState([1000])
  const [duration, setDuration] = useState([2.5])
  const [startTime, setStartTime] = useState("18:00")
  const [people, setPeople] = useState(2)
  const [studentDiscount, setStudentDiscount] = useState(false)
  const [drinkBar, setDrinkBar] = useState(false)

  const [membershipSettings, setMembershipSettings] = useState<MembershipSettings>({
    karaokeCan: { isMember: false },
    bigEcho: { isMember: false },
    tetsuJin: { isMember: false },
    manekineko: { isMember: false },
    jankara: { isMember: false },
    utahiroba: { isMember: false },
  })

  const updateMembership = (chainKey: string, isMember: boolean) => {
    setMembershipSettings((prev) => ({
      ...prev,
      [chainKey]: { isMember },
    }))
  }

  const chainKeyToName: Record<string, string> = {
    karaokeCan: "カラオケ館",
    bigEcho: "ビッグエコー",
    tetsuJin: "カラオケの鉄人",
    manekineko: "まねきねこ",
    jankara: "ジャンカラ",
    utahiroba: "歌広場",
  }

  const chainNameToKey: Record<string, string> = {
    カラオケ館: "karaokeCan",
    ビッグエコー: "bigEcho",
    カラオケの鉄人: "tetsuJin",
    まねきねこ: "manekineko",
    ジャンカラ: "jankara",
    歌広場: "utahiroba",
    パセラ: "pasela",
  }

  const handleSearch = async () => {
    try {
      const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000"
      const memberNames = Object.entries(membershipSettings)
        .filter(([, v]) => v.isMember)
        .map(([k]) => chainKeyToName[k])

      const payload = {
        latitude: coords.lat ?? 35.6595,
        longitude: coords.lng ?? 139.7005,
        stay_minutes: Math.round(duration[0] * 60),
        is_free_time: false,
        start_time: startTime,
        group_size: people,
        is_student: studentDiscount,
        member_shop_ids: memberNames,
        radius: distance[0],
      }

      const res = await fetch(`${apiBase}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })

      if (res.ok) {
        const data = await res.json()
        const newStores: Store[] = (data.results || []).map((s: any) => ({
          id: s.shop_id,
          name: s.name,
          chain: s.icon_url,
          price: s.price_per_person,
          badges: s.all_plans,
          phone: s.phone,
          chainKey: chainNameToKey[s.icon_url] || s.icon_url,
          duration: `${duration[0]}時間`,
        }))
        setStores(newStores)
      }
      setCurrentView("results")
    } catch (e) {
      console.error(e)
      setStores(mockStores)
      setCurrentView("results")
    }
  }

  const handleUseCurrentLocation = () => {
    if (navigator.geolocation) {
      setSearchLocation("現在地を取得中...")
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setCoords({ lat: pos.coords.latitude, lng: pos.coords.longitude })
          setSearchLocation("現在地")
        },
        () => {
          setSearchLocation("位置情報を取得できませんでした")
        }
      )
    } else {
      setSearchLocation("位置情報未対応")
    }
  }

  const handleStoreSelect = async (store: Store) => {
    try {
      const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000"
      const memberNames = Object.entries(membershipSettings)
        .filter(([, v]) => v.isMember)
        .map(([k]) => chainKeyToName[k])
      const res = await fetch(`${apiBase}/get_detail`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          shop_id: store.id,
          start_time: startTime,
          stay_minutes: Math.round(duration[0] * 60),
          is_student: studentDiscount,
          member_shop_ids: memberNames,
        }),
      })
      if (res.ok) {
        const detail = await res.json()
        setSelectedStore({ ...store, plans: detail.plans as PlanDetail[] })
      } else {
        setSelectedStore(store)
      }
    } catch (e) {
      console.error(e)
      setSelectedStore(store)
    }
  }

  if (currentView === "home") {
    return (
      <SearchPage
        searchLocation={searchLocation}
        setSearchLocation={setSearchLocation}
        distance={distance}
        setDistance={setDistance}
        startTime={startTime}
        setStartTime={setStartTime}
        duration={duration}
        setDuration={setDuration}
        people={people}
        setPeople={setPeople}
        studentDiscount={studentDiscount}
        setStudentDiscount={setStudentDiscount}
        drinkBar={drinkBar}
        setDrinkBar={setDrinkBar}
        onSearch={handleSearch}
        onUseCurrentLocation={handleUseCurrentLocation}
        membershipSettings={membershipSettings}
        updateMembership={updateMembership}
      />
    )
  }

  return (
    <>
      <ResultsPage
        onBack={() => setCurrentView("home")}
        viewMode={viewMode}
        setViewMode={setViewMode}
        stores={stores}
        searchLocation={searchLocation}
        distance={distance}
        startTime={startTime}
        duration={duration}
        people={people}
        studentDiscount={studentDiscount}
        membershipSettings={membershipSettings}
        onStoreSelect={handleStoreSelect}
      />
      <StoreDetail
        store={selectedStore}
        onClose={() => setSelectedStore(null)}
        membershipSettings={membershipSettings}
      />
    </>
  )
}
