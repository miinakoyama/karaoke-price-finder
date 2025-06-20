"use client"

import { useState } from "react"
import { SearchPage } from "./pages/SearchPage"
import { ResultsPage } from "./pages/ResultsPage"
import { StoreDetail } from "./pages/StoreDetail"
import { Store, MembershipSettings } from "./types/store"

export default function KaraokeSearchApp() {
  const [currentView, setCurrentView] = useState<"home" | "results">("home")
  const [viewMode, setViewMode] = useState<"list" | "map">("list")
  const [selectedStore, setSelectedStore] = useState<Store | null>(null)
  const [searchLocation, setSearchLocation] = useState("")
  const [distance, setDistance] = useState([1000])
  const [duration, setDuration] = useState([2.5])
  const [startTime, setStartTime] = useState("18:00")
  const [people, setPeople] = useState(2)
  const [studentDiscount, setStudentDiscount] = useState(false)
  const [drinkBar, setDrinkBar] = useState(false)
  const [stores, setStores] = useState<Store[]>([])

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

  const handleSearch = async () => {
    const body = {
      latitude: undefined,
      longitude: undefined,
      place_name: searchLocation,
      stay_minutes: Math.round(duration[0] * 60),
      is_free_time: false,
      start_time: startTime,
      group_size: people,
      is_student: studentDiscount,
      member_shop_ids: Object.entries(membershipSettings)
        .filter(([, v]) => v.isMember)
        .map(([k]) => k),
      radius: distance[0],
    }
    try {
      const res = await fetch("http://localhost:8000/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      })
      if (!res.ok) throw new Error("検索APIエラー")
      const data = await res.json()
      setStores(data.results.map(mapApiShopToStore))
      setCurrentView("results")
    } catch (e) {
      alert("検索に失敗しました")
    }
  }

  function getChainKey(chainName: string): string {
    switch (chainName) {
      case "カラオケ館": return "karaokeCan";
      case "ビッグエコー": return "bigEcho";
      case "カラオケの鉄人": return "tetsuJin";
      case "まねきねこ": return "manekineko";
      case "ジャンカラ": return "jankara";
      case "歌広場": return "utahiroba";
      default: return "karaokeCan";
    }
  }

  function mapApiShopToStore(apiShop: any): Store {
    const chainKey = getChainKey(apiShop.icon_url || apiShop.chain_name || "");
    return {
      id: apiShop.shop_id,
      name: apiShop.name,
      chain: apiShop.icon_url || "",
      price: apiShop.price_per_person,
      memberPrice: undefined,
      drinkInfo: "ドリンクバー付",
      badges: [],
      distance: "0.5km",
      rating: 4.0,
      address: "住所未設定",
      phone: apiShop.phone || "",
      features: [],
      chainKey,
      latitude: apiShop.latitude || 0,
      longitude: apiShop.longitude || 0,
    }
  }

  const handleUseCurrentLocation = () => {
    setSearchLocation("現在地を取得中...")
    setTimeout(() => {
      setSearchLocation("東京都渋谷区")
    }, 1000)
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
        onStoreSelect={setSelectedStore}
      />
      <StoreDetail
        store={selectedStore}
        onClose={() => setSelectedStore(null)}
        membershipSettings={membershipSettings}
      />
    </>
  )
}
