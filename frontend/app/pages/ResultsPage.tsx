import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Map, List, Navigation, Star, Search } from "lucide-react"
import { ResultsMap } from "@/components/ResultsMap"
import { Store, MembershipSettings } from "../types/store"
import { PlanDetail, GetDetailResponse } from "../types/api"
import Image from "next/image"
import { useState } from "react"
import { StoreDetail } from "./StoreDetail"

interface ResultsPageProps {
  onBack: () => void
  viewMode: "list" | "map"
  setViewMode: (mode: "list" | "map") => void
  stores: Store[]
  searchLocation: string
  searchLatitude: number | null
  searchLongitude: number | null
  distance: number[]
  startTime: string
  duration: number[]
  people: number
  studentDiscount: boolean
  membershipSettings: MembershipSettings
  onStoreSelect: (store: Store) => void
}

export function ResultsPage({
  onBack,
  viewMode,
  setViewMode,
  stores,
  searchLocation,
  searchLatitude,
  searchLongitude,
  distance,
  startTime,
  duration,
  people,
  studentDiscount,
  membershipSettings,
  onStoreSelect,
}: ResultsPageProps) {
  const [selectedStore, setSelectedStore] = useState<Store | null>(null)
  // 追加: 詳細データ状態
  const [detailData, setDetailData] = useState<GetDetailResponse | null>(null)
  const [loadingDetail, setLoadingDetail] = useState(false)

  const formatDuration = (hours: number) => {
    const h = Math.floor(hours)
    const m = Math.round((hours - h) * 60)
    if (h === 0) return `${m}分`
    if (m === 0) return `${h}時間`
    return `${h}時間${m}分`
  }

  const formatDistance = (d: number) => {
    if (d === 500) return `${d}m以内`
    return `${d / 1000}km以内`
  }

  const chainNameMap: Record<string, string> = {
    karaokeCan: 'カラオケ館',
    bigEcho: 'ビッグエコー',
    tetsuJin: 'カラオケの鉄人',
    manekineko: 'まねきねこ',
    jankara: 'ジャンカラ',
    utahiroba: '歌広場',
  }

  const chainLogoMap: Record<string, string> = {
    karaokeCan: '/karaokeCan.png',
    bigEcho: '/bigEcho.jpeg',
    tetsuJin: '/karaokeTetsujin.jpeg',
    manekineko: '/manekiNeko.jpg',
    jankara: '/jyanKara.jpg',
    utahiroba: '/utahiroba.jpeg',
  }

  const memberStoreLabel = Object.entries(membershipSettings)
    .filter(([, v]) => v.isMember)
    .map(([k]) => chainNameMap[k] || k)
    .join('、')

  // 店舗選択時に詳細APIを呼ぶ
  const handleStoreSelect = async (store: Store) => {
    setSelectedStore(store)
    setLoadingDetail(true)
    setDetailData(null)
    try {
      const res = await fetch("http://localhost:8000/get_detail", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          shop_id: store.shop_id,
          start_time: startTime,
          stay_minutes: Math.round(duration[0] * 60),
          is_student: studentDiscount,
          member_shop_ids: Object.entries(membershipSettings)
            .filter(([, v]) => v.isMember)
            .map(([k]) => k),
        }),
      })
      if (!res.ok) throw new Error("詳細APIエラー")
      const data = await res.json()
      setDetailData(data)
    } catch (e) {
      alert("詳細取得に失敗しました")
    } finally {
      setLoadingDetail(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-white border-b border-gray-200 px-4 py-3 flex items-center gap-3">
        <Button variant="ghost" size="icon" onClick={onBack}>
          ←
        </Button>
        <h1 className="font-semibold text-gray-900">検索結果</h1>
      </header>

      {/* Filter Chips */}
      <div className="px-4 py-3 bg-white border-b">
        <div className="flex flex-wrap gap-2">
          <Badge variant="outline" className="whitespace-nowrap">
            {searchLocation || "場所未指定"}
          </Badge>
          <Badge variant="outline" className="whitespace-nowrap">
            {`距離 ${formatDistance(distance[0])}`}
          </Badge>
          <Badge variant="outline" className="whitespace-nowrap">
            {`開始 ${startTime}`}
          </Badge>
          <Badge variant="outline" className="whitespace-nowrap">
            {`利用 ${formatDuration(duration[0])}`}
          </Badge>
          <Badge variant="outline" className="whitespace-nowrap">
            {`${people}人`}
          </Badge>
          <Badge variant="outline" className="whitespace-nowrap">
            {studentDiscount ? "学割利用" : "学割なし"}
          </Badge>
          {memberStoreLabel && (
              <Badge variant="outline" className="whitespace-nowrap">
                {`会員: ${memberStoreLabel}`}
              </Badge>
          )}
        </div>
      </div>

      {/* View Toggle FAB */}
      <Button
        className="fixed bottom-4 right-4 z-40 rounded-full w-14 h-14 bg-indigo-600 hover:bg-indigo-700"
        onClick={() => setViewMode(viewMode === "list" ? "map" : "list")}
      >
        {viewMode === "list" ? <Map className="w-5 h-5" /> : <List className="w-5 h-5" />}
      </Button>

      {/* Results */}
      {viewMode === "list" ? (
        <div className="p-4 space-y-2 pb-20">
          {stores.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-16 text-center">
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                <Search className="w-8 h-8 text-gray-400" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">該当する店が見つかりませんでした</h3>
              <p className="text-gray-500 text-sm max-w-md">
                検索条件を変更して、再度お試しください。
                <br />
                時間帯や距離、会員情報などを調整すると見つかる可能性があります。
              </p>
            </div>
          ) : (
            stores.map((store) => {
              const isMember = membershipSettings[store.chainKey as keyof typeof membershipSettings]?.isMember
              const displayPrice = isMember && store.memberPrice ? store.memberPrice : store.price_per_person

              return (

                <Card key={store.shop_id} className="shadow-sm cursor-pointer hover:shadow-md transition-shadow">
                  <CardContent className="p-3" onClick={() => onStoreSelect(store)}>
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 rounded-full flex items-center justify-center bg-white border relative">
                        <div className="w-12 h-12 rounded-full overflow-hidden">
                          <Image
                            src={chainLogoMap[store.chainKey] || '/placeholder-logo.png'}
                            alt={store.icon_url}
                            width={48}
                            height={48}
                            className="object-contain w-full h-full"
                          />
                        </div>
                        {isMember && (
                          <div className="absolute -bottom-1 -right-1 bg-green-500 border-2 border-white rounded-full w-5 h-5 flex items-center justify-center shadow z-10">
                            <span className="text-white text-[8px] font-bold flex items-center gap-0.5">
                              会員
                            </span>
                          </div>
                        )}
                      </div>
                      <div className="flex-1 min-w-0 flex items-center justify-between">
                        <div className="min-w-0">
                          <h3 className="font-medium text-gray-900 truncate leading-tight">{store.name}</h3>
                          <div className="flex items-center gap-1 text-xs text-gray-500 mt-0.5">
                            <Navigation className="w-3 h-3" />
                            <span>{store.distance}</span>
                          </div>
                        </div>
                        <div className="text-right ml-2 flex flex-col items-end justify-center min-w-[80px]">
                          <div className="text-xl font-bold text-gray-900 leading-tight">
                            ¥{displayPrice.toLocaleString()}
                          </div>
                          <div className="text-xs text-gray-500 mt-0.5">{store.drinkInfo}</div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )
            })
          )}
        </div>
      ) : (
        <div className="h-[calc(100vh-120px)]">
          <ResultsMap
            stores={stores}
            membershipSettings={membershipSettings}
            onMarkerClick={onStoreSelect}
            searchLatitude={searchLatitude}
            searchLongitude={searchLongitude}
            searchLocation={searchLocation}
          />
        </div>
      )}

      {/* StoreDetail モーダル */}
      <StoreDetail
        store={null}
        detailData={null}
        loading={false}
        onClose={() => {}}
        membershipSettings={membershipSettings}
      />
    </div>
  )
}
