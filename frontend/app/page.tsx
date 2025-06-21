"use client"

import { useState, useEffect } from "react"
import { toast } from "sonner"
import { useDebounce } from "use-debounce"
import { SearchPage } from "./pages/SearchPage"
import { ResultsPage } from "./pages/ResultsPage"
import { StoreDetail } from "./pages/StoreDetail"
import { Store, MembershipSettings } from "./types/store"
import { GetDetailResponse } from "./types/api"

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
  const [detailData, setDetailData] = useState<GetDetailResponse | null>(null)
  const [loadingDetail, setLoadingDetail] = useState(false)

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
  
  function getChainKey(chainName: string): string {
    switch (chainName) {
      case "カラオケ館":
      case "karaokeCan":
        return "karaokeCan";
      case "ビッグエコー":
      case "bigEcho":
        return "bigEcho";
      case "カラオケの鉄人":
      case "tetsuJin":
        return "tetsuJin";
      case "まねきねこ":
      case "manekineko":
        return "manekineko";
      case "ジャンカラ":
      case "jankara":
        return "jankara";
      case "歌広場":
      case "utahiroba":
        return "utahiroba";
      default:
        return "karaokeCan";
    }
  }

  function mapApiShopToStore(apiShop: any): Store {
    const chainKey = getChainKey(apiShop.icon_url || apiShop.chain_name || "");
    return {
      shop_id: apiShop.shop_id,
      name: apiShop.name,
      icon_url: apiShop.icon_url || "",
      price_per_person: apiShop.price_per_person,
      memberPrice: undefined,
      drinkInfo: "ドリンクバー付",
      badges: [],
      distance: "0.5km",
      rating: 4.0,
      address: "住所未設定",
      phone: apiShop.phone || "",
      features: [],
      all_plans: apiShop.all_plans || [],
      chainKey,
      latitude: apiShop.latitude || 0,
      longitude: apiShop.longitude || 0,
    }
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
          const formattedAddress = data.results[0].formatted_address
          setSearchLocation(formattedAddress)

          const countryComponent = data.results[0].address_components.find((component: any) =>
            component.types.includes("country")
          )
          if (!countryComponent || countryComponent.long_name !== "Japan") {
            toast.error("日本国内の住所を入力してください。「現在地を使う」を押すか、住所を再度手入力してください。")
            setValidAddress(false)
            return
          }

          const location = data.results[0].geometry.location
          setLatitude(location.lat)
          setLongitude(location.lng)
          setValidAddress(true)
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
        latitude: latitude ?? 35.6646782, // fallback to 日本、〒106-0032 東京都港区六本木３丁目２−１ 住友不動産六本木グランドタワー,
        longitude: longitude ?? 139.7378198,
        place_name: searchLocation,
        stay_minutes: duration[0] * 60, 
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
        setStores((data.results || []).map(mapApiShopToStore))
        setCurrentView("results")
      } catch (error) {
        console.error("検索APIエラー:", error)
      }
    }
  }

  useEffect(() => {
    if (!selectedStore) return;
    setLoadingDetail(true);
    setDetailData(null);
    fetch("http://localhost:8000/get_detail", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        shop_id: selectedStore.shop_id,
        start_time: startTime,
        stay_minutes: Math.round(duration[0] * 60),
        is_student: studentDiscount,
        member_shop_ids: Object.entries(membershipSettings)
          .filter(([, v]) => v.isMember)
          .map(([k]) => k),
      }),
    })
      .then((res) => {
        if (!res.ok) throw new Error("詳細APIエラー");
        return res.json();
      })
      .then((data) => setDetailData(data))
      .catch(() => setDetailData(null))
      .finally(() => setLoadingDetail(false));
  }, [selectedStore, startTime, duration, studentDiscount, membershipSettings]);

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
        detailData={detailData}
        loading={loadingDetail}
        onClose={() => {
          setSelectedStore(null)
          setDetailData(null)
          setLoadingDetail(false)
        }}
        membershipSettings={membershipSettings}
      />
    </>
  )
}
