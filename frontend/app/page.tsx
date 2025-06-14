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
  const [duration, setDuration] = useState([2.5])
  const [people, setPeople] = useState(2)
  const [studentDiscount, setStudentDiscount] = useState(false)
  const [drinkBar, setDrinkBar] = useState(false)

  const [membershipSettings, setMembershipSettings] = useState<MembershipSettings>({
    karaokeCan: { isMember: false, memberNumber: "" },
    bigEcho: { isMember: false, memberNumber: "" },
    tetsuJin: { isMember: false, memberNumber: "" },
    manekineko: { isMember: false, memberNumber: "" },
    jankara: { isMember: false, memberNumber: "" },
    utahiroba: { isMember: false, memberNumber: "" },
  })

  const updateMembership = (chainKey: string, isMember: boolean, memberNumber = "") => {
    setMembershipSettings((prev) => ({
      ...prev,
      [chainKey]: { isMember, memberNumber },
    }))
  }

  const handleSearch = () => {
    setCurrentView("results")
  }

  const handleUseCurrentLocation = () => {
    setSearchLocation("現在地を取得中...")
    // Simulate GPS location fetch
    setTimeout(() => {
      setSearchLocation("東京都渋谷区")
    }, 1000)
  }

  if (currentView === "home") {
    return (
      <SearchPage
        searchLocation={searchLocation}
        setSearchLocation={setSearchLocation}
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
