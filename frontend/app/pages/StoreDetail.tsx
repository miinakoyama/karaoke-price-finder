import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Sheet, SheetContent } from "@/components/ui/sheet"
import { MapPin, Phone, Star, Navigation } from "lucide-react"
import { Store, MembershipSettings } from "../types/store"
import { PlanDetail, GetDetailResponse } from "../types/api"
import Image from "next/image"
import { useState, useEffect } from "react"

interface StoreDetailProps {
  store: Store | null
  detailData?: GetDetailResponse | null
  loading?: boolean
  onClose: () => void
  membershipSettings: MembershipSettings
}

export function StoreDetail({ store, detailData, loading, onClose, membershipSettings }: StoreDetailProps) {
  const [address, setAddress] = useState<string>("")
  const [loadingAddress, setLoadingAddress] = useState(false)

  // 緯度・経度から住所を逆引き
  useEffect(() => {
    if (!store || !store.latitude || !store.longitude) {
      setAddress("住所未設定")
      return
    }

    const fetchAddress = async () => {
      setLoadingAddress(true)
      try {
        const response = await fetch(
          `https://maps.googleapis.com/maps/api/geocode/json?latlng=${store.latitude},${store.longitude}&key=${process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY}`
        )
        const data = await response.json()
        
        if (data.status === "OK" && data.results.length > 0) {
          setAddress(data.results[0].formatted_address)
        } else {
          setAddress("住所未設定")
        }
      } catch (error) {
        console.error("住所取得エラー:", error)
        setAddress("住所未設定")
      } finally {
        setLoadingAddress(false)
      }
    }

    fetchAddress()
  }, [store])

  if (!store) return null

  const isMember = membershipSettings[store.chainKey as keyof typeof membershipSettings]?.isMember
  const memberPrice = store.memberPrice
  const regularPrice = store.price_per_person

  const chainLogoMap: Record<string, string> = {
    karaokeCan: '/karaokeCan.png',
    bigEcho: '/bigEcho.jpeg',
    tetsuJin: '/karaokeTetsujin.jpeg',
    manekineko: '/manekiNeko.jpg',
    jankara: '/jyanKara.jpg',
    utahiroba: '/utahiroba.jpeg',
    pasela: '/pasela.png',
  }

  function customerTypeToJa(type: string): string {
    switch (type) {
      case "general": return "一般";
      case "student": return "学生";
      case "member": return "会員";
      default: return type;
    }
  }

  return (
    <Sheet open={!!store} onOpenChange={onClose}>
      <SheetContent side="bottom" className="h-[90vh] rounded-t-xl overflow-y-auto">
        <div className="py-6 space-y-6">
          {/* Store Header */}
          <div className="text-center">
            <div className="w-16 h-16 rounded-full overflow-hidden flex items-center justify-center mx-auto mb-3 bg-white border">
              <Image
                src={chainLogoMap[store.chainKey] || '/placeholder-logo.png'}
                alt={store.icon_url}
                width={64}
                height={64}
                className="object-contain w-full h-full"
              />
            </div>
            <h2 className="text-xl font-bold text-gray-900">{store.name}</h2>
            <p className="text-gray-500">
              {loadingAddress ? "住所を取得中..." : address}
            </p>
            <div className="flex items-center justify-center gap-1 mt-2">
              <span className="flex items-center gap-1 text-sm text-gray-500">
                <Navigation className="w-4 h-4" />
                {store.distance}
              </span>
            </div>
            {isMember && (
              <Badge variant="default" className="bg-green-500 mt-2">
                会員特典適用中
              </Badge>
            )}
          </div>

          {/* 最安値計算セクション */}
          {store.price_breakdown && store.price_breakdown.length > 0 && (
            <div className="space-y-3">
              <h3 className="font-semibold text-gray-900">最安値計算</h3>
              <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
                {store.price_breakdown.length === 1 ? (
                  // 単一の時間帯の場合
                  <div className="flex justify-between items-center">
                    <div>
                      <div className="text-sm text-gray-600">{store.price_breakdown[0].time_range}</div>
                      <div className="font-medium">{store.price_breakdown[0].plan_name}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-xl font-bold text-orange-600">
                        ¥{store.price_breakdown[0].total_price.toLocaleString()}
                      </div>
                    </div>
                  </div>
                ) : (
                  // 複数の時間帯にまたがる場合
                  <div className="space-y-2">
                    <div className="flex justify-between items-center">
                      <div className="flex-1">
                        {store.price_breakdown.map((calc, idx) => (
                          <div key={idx} className="flex justify-between items-center mb-1">
                            <div className="flex items-center gap-2">
                              <span className="text-sm text-gray-600">{calc.time_range}</span>
                              <span className="font-medium">{calc.plan_name}</span>
                            </div>
                            <div className="text-right">
                              <span className="font-medium">¥{calc.total_price.toLocaleString()}</span>
                              {idx < store.price_breakdown!.length - 1 && (
                                <span className="text-gray-400 ml-2">+</span>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                    <div className="border-t border-orange-200 pt-2 flex justify-between items-center">
                      <span className="font-semibold">合計</span>
                      <span className="text-xl font-bold text-orange-600">
                        ¥{store.price_breakdown.reduce((sum, calc) => sum + calc.total_price, 0).toLocaleString()}
                      </span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Price Table */}
          <div className="space-y-3">
            <h3 className="font-semibold text-gray-900">料金プラン</h3>
            {loading ? (
              <div className="text-center py-8">読み込み中...</div>
            ) : detailData ? (
              <div className="space-y-2">
                {(() => {
                  // プラン名でグループ化
                  const planGroups = detailData.plans.reduce((groups, plan) => {
                    if (!groups[plan.plan_name]) {
                      groups[plan.plan_name] = [];
                    }
                    groups[plan.plan_name].push(plan);
                    return groups;
                  }, {} as Record<string, PlanDetail[]>);

                  return Object.entries(planGroups).map(([planName, plans]) => {
                    // 各プランから有効な価格を取得
                    const prices = {
                      general: plans.find(p => p.general_price !== null)?.general_price,
                      student: plans.find(p => p.student_price !== null)?.student_price,
                      member: plans.find(p => p.member_price !== null)?.member_price,
                    };

                    // 時間帯を取得（最初のプランから）
                    const timeRange = plans[0]?.time_range;

                    // 最安値を計算
                    const validPrices = Object.values(prices).filter(p => p !== null && p !== undefined) as number[];
                    const minPrice = validPrices.length > 0 ? Math.min(...validPrices) : 0;
                    const isCheapest = minPrice === store.price_per_person;

                    return (
                      <div
                        key={planName}
                        className={`flex justify-between items-center p-3 rounded-lg border ${
                          isCheapest
                            ? 'bg-orange-50 border-orange-200 shadow-sm'
                            : 'bg-gray-50 border-gray-200'
                        }`}
                      >
                        <div className="flex items-center gap-2">
                          <span>
                            {planName}
                            {timeRange && ` (${timeRange})`}
                          </span>
                        </div>
                        <div className="flex items-center gap-4">
                          {prices.general !== null && prices.general !== undefined && (
                            <div className="text-right">
                              <div className="text-xs text-gray-500">一般</div>
                              <div className="font-bold text-gray-900">
                                ¥{prices.general.toLocaleString()}
                              </div>
                            </div>
                          )}
                          {prices.student !== null && prices.student !== undefined && (
                            <div className="text-right">
                              <div className="text-xs text-gray-500">学生</div>
                              <div className="font-bold text-gray-900">
                                ¥{prices.student.toLocaleString()}
                              </div>
                            </div>
                          )}
                          {prices.member !== null && prices.member !== undefined && (
                            <div className="text-right">
                              <div className="text-xs text-gray-500">会員</div>
                              <div className="font-bold text-gray-900">
                                ¥{prices.member.toLocaleString()}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    );
                  });
                })()}
              </div>
            ) : (
              <div className="space-y-2">
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
                    <span className={`font-bold ${isMember && memberPrice ? "text-green-600" : "text-orange-600"}`}>
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
              </div>
            )}
          </div>

          {/* Features */}
          <div className="space-y-3">
            <h3 className="font-semibold text-gray-900">サービス</h3>
            <div className="flex flex-wrap gap-2">
              {/* ドリンク情報 */}
              {store.drinkInfo && (
                <Badge variant="secondary" className="bg-blue-100 text-blue-800">
                  {store.drinkInfo}
                </Badge>
              )}
              {/* その他のサービス */}
              {(store.features ?? []).map((feature) => (
                <Badge key={feature} variant="secondary">
                  {feature}
                </Badge>
              ))}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="space-y-3 pt-4">
            <Button 
              className="w-full bg-orange-500 hover:bg-orange-600"
              onClick={() => {
                // Google Mapsで店舗の位置を開く
                const query = address && address !== "住所未設定" 
                  ? `${store.name} ${address}`
                  : `${store.name} ${store.latitude},${store.longitude}`
                const url = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(query)}`
                window.open(url, '_blank')
              }}
            >
              <MapPin className="w-4 h-4 mr-2" />
              地図で開く
            </Button>
            <Button 
              variant="outline" 
              className="w-full"
              onClick={() => {
                // 電話番号に電話をかける
                const phoneNumber = detailData?.phone_number || store.phone;
                if (phoneNumber) {
                  window.location.href = `tel:${phoneNumber}`
                } else {
                  alert('電話番号が登録されていません')
                }
              }}
            >
              <Phone className="w-4 h-4 mr-2" />
              電話する {detailData?.phone_number && `(${detailData.phone_number})`}
            </Button>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  )
}
