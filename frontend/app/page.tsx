"use client"

import { useState, useEffect } from "react"
import { toast } from "sonner"
import { useDebounce } from "use-debounce"
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
  const [stores, setStores] = useState<Store[]>([])
  const [latitude, setLatitude] = useState<number | null>(null)
  const [longitude, setLongitude] = useState<number | null>(null)
  const [inputAddress, setInputAddress] = useState("")
  const [validAddress, setValidAddress] = useState(false)
  const [debouncedAddress] = useDebounce(inputAddress, 1000) // 1秒間入力が止まったら反応
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
  
  const GOOGLE_MAPS_API_KEY = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY

  const handleUseCurrentLocation = () => {
    setSearchLocation("現在地を取得中...")
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords
        setLatitude(latitude)
        setLongitude(longitude)

        try {
          const response = await fetch(
            `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=${GOOGLE_MAPS_API_KEY}`
          )
          const data = await response.json()
          if (data.status === "OK") {
            const address = data.results[0].formatted_address
            setSearchLocation(address)
            setValidAddress(true)
          } else {
            toast.error("住所の取得に失敗しました。再度「現在地を使う」を押すか、住所を手入力してください。")
            setSearchLocation("")
          }
        } catch (error) {
          console.error("Geocodingエラー:", error)
          toast.error("エラーが発生しました。再度「現在地を使う」を押すか、住所を手入力してください。")
          setSearchLocation("")
        }
      },
      (error) => {
        console.error("位置情報エラー:", error)
        toast.error("位置情報の取得に失敗しました。住所を手入力してください。")
        setSearchLocation("")
      }
    )
  }

  useEffect(() => {
    const fetchLatLng = async () => {
      if (!debouncedAddress) return
  
      try {
        const response = await fetch(
          `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(debouncedAddress)}&key=${GOOGLE_MAPS_API_KEY}`
        )
        const data = await response.json()
  
        if (data.status === "OK") {
          const location = data.results[0].geometry.location
          const formattedAddress = data.results[0].formatted_address
          setLatitude(location.lat)
          setLongitude(location.lng)
          setSearchLocation(formattedAddress)
        } else {
          console.log("位置情報の取得に失敗")
          toast.error("無効な住所です。「現在地を使う」を押すか、住所を再度手入力してください。")
          setValidAddress(false)
        }
      } catch (error) {
        console.error("Geocodingエラー:", error)
      }
    }
  
    fetchLatLng()
  }, [debouncedAddress])

  const handleSearch = async () => {  
    console.log(searchLocation, longitude, latitude )
    if (!searchLocation) {
      toast.error("住所が未入力です。「現在地を使う」を押すか、住所を手入力してください。")
    } else if (!validAddress) {
      toast.error("無効な住所です。「現在地を使う」を押すか、住所を再度手入力してください。")
    } else {
      const member_shop_ids = Object.entries(membershipSettings)
        .filter(([, value]) => value.isMember)
        .map(([key]) => key)
      const payload = {
        latitude: latitude ?? 35.6895, // fallback to 渋谷区,
        longitude: longitude ?? 139.6917,
        place_name: searchLocation,
        stay_minutes: duration[0] * 60, 
        is_free_time: false,
        start_time: startTime,
        group_size: people,
        is_student: studentDiscount,
        member_shop_ids: member_shop_ids,
        radius: distance[0],
      }

      try {
        const response = await fetch("http://localhost:8000/search", {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        })
    
        const data = await response.json()
        setStores(data.results || [])
        setCurrentView("results")
      } catch (error) {
        console.error("検索APIエラー:", error)
      }
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
        inputAddress={inputAddress}
        setInputAddress={setInputAddress}
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
