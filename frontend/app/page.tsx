"use client"

import { useState } from "react"
import { SearchPage } from "./pages/SearchPage"
import { ResultsPage } from "./pages/ResultsPage"
import { StoreDetail } from "./pages/StoreDetail"
import { Store, MembershipSettings, mockStores } from "./types/store"

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

  const handleSearch = () => {
    setCurrentView("results")
  }

  const GOOGLE_MAPS_API_KEY = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY

  const handleUseCurrentLocation = () => {
    setSearchLocation("現在地を取得中...")

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords
        console.log("位置情報:", { latitude, longitude })

        try {
          const response = await fetch(
            `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=${GOOGLE_MAPS_API_KEY}`
          )
          const data = await response.json()

          if (data.status === "OK") {
            const address = data.results[0].formatted_address
            setSearchLocation(address)
          } else {
            setSearchLocation("住所の取得に失敗しました")
          }
        } catch (error) {
          console.error("Geocodingエラー:", error)
          setSearchLocation("エラーが発生しました")
        }
      },
      (error) => {
        console.error("位置情報エラー:", error)
        setSearchLocation("位置情報の取得に失敗しました")
      }
    )
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
        stores={mockStores}
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
