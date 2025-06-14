"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import { Slider } from "@/components/ui/slider"
import { Badge } from "@/components/ui/badge"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { MapPin, Search, Clock, Users, Menu, ChevronDown, Phone, Star, Navigation, Map, List } from "lucide-react"

// Storeインターフェースを更新（既存のStoreインターフェースを以下に置き換え）
interface Store {
  id: string
  name: string
  chain: string
  price: number
  memberPrice?: number
  duration: string
  badges: string[]
  distance: string
  rating: number
  address: string
  phone: string
  features: string[]
  chainKey: string
}

// mockStoresデータを更新（会員価格を追加）
const mockStores: Store[] = [
  {
    id: "1",
    name: "カラオケ館 渋谷本店",
    chain: "カラオケ館",
    price: 1280,
    memberPrice: 1080,
    duration: "2時間・1ドリンク付",
    badges: ["最安", "学割OK"],
    distance: "0.3km",
    rating: 4.2,
    address: "東京都渋谷区道玄坂2-10-7",
    phone: "03-1234-5678",
    features: ["ドリンクバー付", "学割あり", "24時間営業"],
    chainKey: "karaokeCan",
  },
  {
    id: "2",
    name: "ビッグエコー 新宿東口店",
    chain: "ビッグエコー",
    price: 1480,
    memberPrice: 1280,
    duration: "2時間・ワンドリンク必須",
    badges: ["学割OK"],
    distance: "0.5km",
    rating: 4.0,
    address: "東京都新宿区新宿3-15-8",
    phone: "03-2345-6789",
    features: ["学割あり", "フリータイム"],
    chainKey: "bigEcho",
  },
  {
    id: "3",
    name: "カラオケの鉄人 池袋店",
    chain: "カラオケの鉄人",
    price: 1680,
    memberPrice: 1480,
    duration: "2時間・ドリンクバー付",
    badges: ["ドリンクバー付"],
    distance: "0.8km",
    rating: 4.5,
    address: "東京都豊島区南池袋1-20-1",
    phone: "03-3456-7890",
    features: ["ドリンクバー付", "深夜パック"],
    chainKey: "tetsuJin",
  },
]

export default function KaraokeSearchApp() {
  const [currentView, setCurrentView] = useState<"home" | "results">("home")
  const [viewMode, setViewMode] = useState<"list" | "map">("list")
  const [selectedStore, setSelectedStore] = useState<Store | null>(null)
  const [searchLocation, setSearchLocation] = useState("")
  const [duration, setDuration] = useState([2.5])
  const [people, setPeople] = useState(2)
  const [studentDiscount, setStudentDiscount] = useState(false)
  const [drinkBar, setDrinkBar] = useState(false)
  const [drawerOpen, setDrawerOpen] = useState(false)

  // stateの追加（既存のstateの後に追加）
  const [membershipSettings, setMembershipSettings] = useState({
    karaokeCan: { isMember: false, memberNumber: "" },
    bigEcho: { isMember: false, memberNumber: "" },
    tetsuJin: { isMember: false, memberNumber: "" },
    manekineko: { isMember: false, memberNumber: "" },
    jankara: { isMember: false, memberNumber: "" },
    utahiroba: { isMember: false, memberNumber: "" },
  })

  // 会員設定を更新する関数を追加
  const updateMembership = (chainKey: string, isMember: boolean, memberNumber = "") => {
    setMembershipSettings((prev) => ({
      ...prev,
      [chainKey]: { isMember, memberNumber },
    }))
  }

  const formatDuration = (hours: number) => {
    const h = Math.floor(hours)
    const m = Math.round((hours - h) * 60)
    if (h === 0) return `${m}分`
    if (m === 0) return `${h}時間`
    return `${h}時間${m}分`
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
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="sticky top-0 z-50 bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">K</span>
            </div>
            <span className="font-semibold text-gray-900">カラオケ最安検索</span>
          </div>
          <Sheet open={drawerOpen} onOpenChange={setDrawerOpen}>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon">
                <Menu className="w-5 h-5" />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-80">
              <div className="py-6">
                <h2 className="text-lg font-semibold mb-6">設定</h2>
                <div className="space-y-6">
                  {/* 会員設定セクション */}
                  <div className="space-y-4">
                    <h3 className="text-base font-semibold text-gray-900 border-b pb-2">会員設定</h3>

                    {/* カラオケ館 */}
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium">カラオケ館</span>
                        <Button
                          variant={membershipSettings.karaokeCan.isMember ? "default" : "outline"}
                          size="sm"
                          onClick={() => updateMembership("karaokeCan", !membershipSettings.karaokeCan.isMember)}
                        >
                          {membershipSettings.karaokeCan.isMember ? "会員" : "非会員"}
                        </Button>
                      </div>
                      {membershipSettings.karaokeCan.isMember && (
                        <Input
                          placeholder="会員番号を入力"
                          value={membershipSettings.karaokeCan.memberNumber}
                          onChange={(e) => updateMembership("karaokeCan", true, e.target.value)}
                          className="text-sm"
                        />
                      )}
                    </div>

                    {/* ビッグエコー */}
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium">ビッグエコー</span>
                        <Button
                          variant={membershipSettings.bigEcho.isMember ? "default" : "outline"}
                          size="sm"
                          onClick={() => updateMembership("bigEcho", !membershipSettings.bigEcho.isMember)}
                        >
                          {membershipSettings.bigEcho.isMember ? "会員" : "非会員"}
                        </Button>
                      </div>
                      {membershipSettings.bigEcho.isMember && (
                        <Input
                          placeholder="会員番号を入力"
                          value={membershipSettings.bigEcho.memberNumber}
                          onChange={(e) => updateMembership("bigEcho", true, e.target.value)}
                          className="text-sm"
                        />
                      )}
                    </div>

                    {/* カラオケの鉄人 */}
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium">カラオケの鉄人</span>
                        <Button
                          variant={membershipSettings.tetsuJin.isMember ? "default" : "outline"}
                          size="sm"
                          onClick={() => updateMembership("tetsuJin", !membershipSettings.tetsuJin.isMember)}
                        >
                          {membershipSettings.tetsuJin.isMember ? "会員" : "非会員"}
                        </Button>
                      </div>
                      {membershipSettings.tetsuJin.isMember && (
                        <Input
                          placeholder="会員番号を入力"
                          value={membershipSettings.tetsuJin.memberNumber}
                          onChange={(e) => updateMembership("tetsuJin", true, e.target.value)}
                          className="text-sm"
                        />
                      )}
                    </div>

                    {/* まねきねこ */}
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium">まねきねこ</span>
                        <Button
                          variant={membershipSettings.manekineko.isMember ? "default" : "outline"}
                          size="sm"
                          onClick={() => updateMembership("manekineko", !membershipSettings.manekineko.isMember)}
                        >
                          {membershipSettings.manekineko.isMember ? "会員" : "非会員"}
                        </Button>
                      </div>
                      {membershipSettings.manekineko.isMember && (
                        <Input
                          placeholder="会員番号を入力"
                          value={membershipSettings.manekineko.memberNumber}
                          onChange={(e) => updateMembership("manekineko", true, e.target.value)}
                          className="text-sm"
                        />
                      )}
                    </div>

                    {/* ジャンカラ */}
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium">ジャンカラ</span>
                        <Button
                          variant={membershipSettings.jankara.isMember ? "default" : "outline"}
                          size="sm"
                          onClick={() => updateMembership("jankara", !membershipSettings.jankara.isMember)}
                        >
                          {membershipSettings.jankara.isMember ? "会員" : "非会員"}
                        </Button>
                      </div>
                      {membershipSettings.jankara.isMember && (
                        <Input
                          placeholder="会員番号を入力"
                          value={membershipSettings.jankara.memberNumber}
                          onChange={(e) => updateMembership("jankara", true, e.target.value)}
                          className="text-sm"
                        />
                      )}
                    </div>

                    {/* 歌広場 */}
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium">歌広場</span>
                        <Button
                          variant={membershipSettings.utahiroba.isMember ? "default" : "outline"}
                          size="sm"
                          onClick={() => updateMembership("utahiroba", !membershipSettings.utahiroba.isMember)}
                        >
                          {membershipSettings.utahiroba.isMember ? "会員" : "非会員"}
                        </Button>
                      </div>
                      {membershipSettings.utahiroba.isMember && (
                        <Input
                          placeholder="会員番号を入力"
                          value={membershipSettings.utahiroba.memberNumber}
                          onChange={(e) => updateMembership("utahiroba", true, e.target.value)}
                          className="text-sm"
                        />
                      )}
                    </div>
                  </div>

                  {/* 一般設定セクション */}
                  <div className="space-y-4">
                    <h3 className="text-base font-semibold text-gray-900 border-b pb-2">一般設定</h3>

                    <div className="flex items-center justify-between">
                      <span>ダークモード</span>
                      <Button variant="outline" size="sm">
                        オフ
                      </Button>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>デフォルト人数</span>
                      <div className="flex items-center gap-2">
                        <Button variant="outline" size="sm" onClick={() => setPeople(Math.max(1, people - 1))}>
                          -
                        </Button>
                        <span className="w-8 text-center">{people}</span>
                        <Button variant="outline" size="sm" onClick={() => setPeople(people + 1)}>
                          +
                        </Button>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>ドリンクバーを常に含む</span>
                      <Button
                        variant={drinkBar ? "default" : "outline"}
                        size="sm"
                        onClick={() => setDrinkBar(!drinkBar)}
                      >
                        {drinkBar ? "オン" : "オフ"}
                      </Button>
                    </div>
                  </div>

                  <div className="pt-4 border-t space-y-3">
                    <Button variant="ghost" className="w-full justify-start">
                      このアプリについて
                    </Button>
                    <Button variant="ghost" className="w-full justify-start">
                      フィードバック送信
                    </Button>
                    <Button variant="ghost" className="w-full justify-start">
                      プライバシー
                    </Button>
                  </div>
                </div>
              </div>
            </SheetContent>
          </Sheet>
        </header>

        {/* Search Card */}
        <div className="p-4">
          <Card className="shadow-sm">
            <CardContent className="p-4 space-y-4">
              {/* Location */}
              <div className="space-y-2">
                <Button variant="outline" className="w-full justify-start gap-2" onClick={handleUseCurrentLocation}>
                  <MapPin className="w-4 h-4" />
                  現在地を使う
                </Button>
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <Input
                    placeholder="住所を入力"
                    className="pl-10"
                    value={searchLocation}
                    onChange={(e) => setSearchLocation(e.target.value)}
                  />
                </div>
              </div>

              {/* Time and Duration */}
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium flex items-center gap-1">
                    <Clock className="w-4 h-4" />
                    開始時間
                  </label>
                  <Input type="time" defaultValue="18:00" />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">利用時間</label>
                  <div className="px-2">
                    <Slider
                      value={duration}
                      onValueChange={setDuration}
                      max={8}
                      min={0.5}
                      step={0.5}
                      className="w-full"
                    />
                    <div className="flex justify-between text-xs text-gray-500 mt-1">
                      <span>30分</span>
                      <Badge variant="secondary" className="text-xs">
                        {formatDuration(duration[0])}
                      </Badge>
                      <span>8時間</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* People Count */}
              <div className="space-y-2">
                <label className="text-sm font-medium flex items-center gap-1">
                  <Users className="w-4 h-4" />
                  人数
                </label>
                <div className="flex items-center gap-3">
                  <Button variant="outline" size="sm" onClick={() => setPeople(Math.max(1, people - 1))}>
                    -
                  </Button>
                  <span className="w-8 text-center font-medium">{people}</span>
                  <Button variant="outline" size="sm" onClick={() => setPeople(people + 1)}>
                    +
                  </Button>
                </div>
              </div>

              {/* Options */}
              <div className="flex gap-2 flex-wrap">
                <Button
                  variant={studentDiscount ? "default" : "outline"}
                  size="sm"
                  onClick={() => setStudentDiscount(!studentDiscount)}
                  className={studentDiscount ? "bg-orange-500 hover:bg-orange-600" : ""}
                >
                  学割
                </Button>
                <Button
                  variant={drinkBar ? "default" : "outline"}
                  size="sm"
                  onClick={() => setDrinkBar(!drinkBar)}
                  className={drinkBar ? "bg-orange-500 hover:bg-orange-600" : ""}
                >
                  ドリンクバー希望
                </Button>
              </div>

              {/* Search Button */}
              <Button className="w-full bg-orange-500 hover:bg-orange-600" onClick={handleSearch}>
                料金を比較
              </Button>
            </CardContent>
          </Card>

          {/* Help Hint */}
          <div className="flex items-center justify-center gap-1 mt-4 text-sm text-gray-500">
            <ChevronDown className="w-4 h-4" />
            使い方を見る
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-white border-b border-gray-200 px-4 py-3 flex items-center gap-3">
        <Button variant="ghost" size="icon" onClick={() => setCurrentView("home")}>
          ←
        </Button>
        <h1 className="font-semibold text-gray-900">検索結果</h1>
      </header>

      {/* Filter Chips */}
      <div className="px-4 py-3 bg-white border-b">
        <div className="flex gap-2 overflow-x-auto">
          <Badge variant="outline" className="whitespace-nowrap">
            半径1km以内
          </Badge>
          <Badge variant="outline" className="whitespace-nowrap">
            24時間営業
          </Badge>
          <Badge variant="outline" className="whitespace-nowrap">
            フリータイム
          </Badge>
          <Badge variant="outline" className="whitespace-nowrap">
            学割対応
          </Badge>
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
        <div className="p-4 space-y-3 pb-20">
          {mockStores.map((store) => {
            const isMember = membershipSettings[store.chainKey as keyof typeof membershipSettings]?.isMember
            const displayPrice = isMember && store.memberPrice ? store.memberPrice : store.price
            const hasMemberDiscount = isMember && store.memberPrice && store.memberPrice < store.price

            return (
              <Card key={store.id} className="shadow-sm cursor-pointer hover:shadow-md transition-shadow">
                <CardContent className="p-4" onClick={() => setSelectedStore(store)}>
                  <div className="flex items-start gap-3">
                    <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center">
                      <span className="text-indigo-600 font-bold text-sm">{store.chain.charAt(0)}</span>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-2">
                        <div>
                          <h3 className="font-medium text-gray-900 truncate">{store.name}</h3>
                          <div className="flex items-center gap-1 mt-1 flex-wrap">
                            {store.badges.map((badge) => (
                              <Badge
                                key={badge}
                                variant={badge === "最安" ? "default" : "secondary"}
                                className={badge === "最安" ? "bg-orange-500" : ""}
                              >
                                {badge}
                              </Badge>
                            ))}
                            {isMember && (
                              <Badge variant="default" className="bg-green-500">
                                会員
                              </Badge>
                            )}
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="flex items-center gap-1">
                            {hasMemberDiscount && (
                              <div className="text-sm text-gray-400 line-through">¥{store.price.toLocaleString()}</div>
                            )}
                            <div
                              className={`text-2xl font-bold ${hasMemberDiscount ? "text-green-600" : "text-gray-900"}`}
                            >
                              ¥{displayPrice.toLocaleString()}
                            </div>
                          </div>
                          <div className="text-sm text-gray-500">{store.duration}</div>
                          {hasMemberDiscount && (
                            <div className="text-xs text-green-600 font-medium">
                              ¥{(store.price - store.memberPrice).toLocaleString()}お得
                            </div>
                          )}
                        </div>
                      </div>
                      <div className="flex items-center justify-between mt-2 text-sm text-gray-500">
                        <div className="flex items-center gap-1">
                          <Navigation className="w-3 h-3" />
                          {store.distance}
                        </div>
                        <div className="flex items-center gap-1">
                          <Star className="w-3 h-3 fill-yellow-400 text-yellow-400" />
                          {store.rating}
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>
      ) : (
        <div className="h-[calc(100vh-120px)] bg-gray-200 flex items-center justify-center">
          <div className="text-center">
            <Map className="w-12 h-12 mx-auto text-gray-400 mb-2" />
            <p className="text-gray-500">マップビュー</p>
            <p className="text-sm text-gray-400">Google Maps統合</p>
          </div>
        </div>
      )}

      {/* Store Detail Sheet */}
      {selectedStore && (
        <Sheet open={!!selectedStore} onOpenChange={() => setSelectedStore(null)}>
          <SheetContent side="bottom" className="h-[90vh] rounded-t-xl">
            <div className="py-6 space-y-6">
              {/* Store Header */}
              <div className="text-center">
                <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-3">
                  <span className="text-indigo-600 font-bold text-xl">{selectedStore.chain.charAt(0)}</span>
                </div>
                <h2 className="text-xl font-bold text-gray-900">{selectedStore.name}</h2>
                <p className="text-gray-500">{selectedStore.address}</p>
                <div className="flex items-center justify-center gap-1 mt-2">
                  <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                  <span className="font-medium">{selectedStore.rating}</span>
                  <span className="text-gray-500">({selectedStore.distance})</span>
                </div>
                {membershipSettings[selectedStore.chainKey as keyof typeof membershipSettings]?.isMember && (
                  <Badge variant="default" className="bg-green-500 mt-2">
                    会員特典適用中
                  </Badge>
                )}
              </div>

              {/* Price Table */}
              <div className="space-y-3">
                <h3 className="font-semibold text-gray-900">料金プラン</h3>
                <div className="space-y-2">
                  {(() => {
                    const isMember =
                      membershipSettings[selectedStore.chainKey as keyof typeof membershipSettings]?.isMember
                    const memberPrice = selectedStore.memberPrice
                    const regularPrice = selectedStore.price

                    return (
                      <>
                        <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                          <span>30分</span>
                          <div className="text-right">
                            {isMember && <div className="text-sm text-gray-400 line-through">¥580</div>}
                            <span className="font-medium">¥{isMember ? "480" : "580"}</span>
                          </div>
                        </div>
                        <div className="flex justify-between items-center p-3 bg-orange-50 rounded-lg border border-orange-200">
                          <span>2時間パック</span>
                          <div className="text-right">
                            {isMember && memberPrice && memberPrice < regularPrice && (
                              <div className="text-sm text-gray-400 line-through">¥{regularPrice.toLocaleString()}</div>
                            )}
                            <span
                              className={`font-bold ${isMember && memberPrice ? "text-green-600" : "text-orange-600"}`}
                            >
                              ¥{(isMember && memberPrice ? memberPrice : regularPrice).toLocaleString()}
                            </span>
                          </div>
                        </div>
                        <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                          <span>フリータイム</span>
                          <div className="text-right">
                            {isMember && <div className="text-sm text-gray-400 line-through">¥2,980</div>}
                            <span className="font-medium">¥{isMember ? "2,480" : "2,980"}</span>
                          </div>
                        </div>
                        <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                          <span>深夜パック</span>
                          <div className="text-right">
                            {isMember && <div className="text-sm text-gray-400 line-through">¥1,980</div>}
                            <span className="font-medium">¥{isMember ? "1,680" : "1,980"}</span>
                          </div>
                        </div>
                      </>
                    )
                  })()}
                </div>
              </div>

              {/* Features */}
              <div className="space-y-3">
                <h3 className="font-semibold text-gray-900">サービス</h3>
                <div className="flex flex-wrap gap-2">
                  {selectedStore.features.map((feature) => (
                    <Badge key={feature} variant="secondary">
                      {feature}
                    </Badge>
                  ))}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="space-y-3 pt-4">
                <Button className="w-full bg-orange-500 hover:bg-orange-600">
                  <MapPin className="w-4 h-4 mr-2" />
                  地図で開く
                </Button>
                <Button variant="outline" className="w-full">
                  <Phone className="w-4 h-4 mr-2" />
                  電話する
                </Button>
              </div>
            </div>
          </SheetContent>
        </Sheet>
      )}
    </div>
  )
}
