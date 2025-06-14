import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Map, List, Navigation, Star } from "lucide-react"
import { Store, MembershipSettings } from "../types/store"

interface ResultsPageProps {
  onBack: () => void
  viewMode: "list" | "map"
  setViewMode: (mode: "list" | "map") => void
  stores: Store[]
  membershipSettings: MembershipSettings
  onStoreSelect: (store: Store) => void
}

export function ResultsPage({
  onBack,
  viewMode,
  setViewMode,
  stores,
  membershipSettings,
  onStoreSelect,
}: ResultsPageProps) {
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
          {stores.map((store) => {
            const isMember = membershipSettings[store.chainKey as keyof typeof membershipSettings]?.isMember
            const displayPrice = isMember && store.memberPrice ? store.memberPrice : store.price
            const hasMemberDiscount = isMember && store.memberPrice && store.memberPrice < store.price

            return (
              <Card key={store.id} className="shadow-sm cursor-pointer hover:shadow-md transition-shadow">
                <CardContent className="p-4" onClick={() => onStoreSelect(store)}>
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
                          {hasMemberDiscount && store.memberPrice && (
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
    </div>
  )
} 