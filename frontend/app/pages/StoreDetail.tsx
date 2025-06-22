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

          {/* Price Table */}
          <div className="space-y-3">
            <h3 className="font-semibold text-gray-900">料金プラン</h3>
            {loading ? (
              <div className="text-center py-8">読み込み中...</div>
            ) : detailData ? (
              <div className="space-y-2">
                {detailData.plans.map((plan: PlanDetail, idx: number) => {
                  // 会員・学生・一般の順で価格を決定
                  const isMember = membershipSettings[store.chainKey as keyof typeof membershipSettings]?.isMember;
                  const isStudent = false; // 学生情報は別途管理が必要

                  let displayPrice = 0;
                  let priceType = "";

                  if (isMember && plan.member_price !== null) {
                    displayPrice = plan.member_price;
                    priceType = "会員";
                  } else if (isStudent && plan.student_price !== null) {
                    displayPrice = plan.student_price;
                    priceType = "学生";
                  } else if (plan.general_price !== null) {
                    displayPrice = plan.general_price;
                    priceType = "一般";
                  }

                  const isCheapest = displayPrice === store.price_per_person;

                  return (
                    <div
                      key={idx}
                      className={`flex justify-between items-center p-3 rounded-lg border ${
                        isCheapest
                          ? 'bg-orange-50 border-orange-200 shadow-sm'
                          : 'bg-gray-50 border-gray-200'
                      }`}
                    >
                      {/* プラン名 */}
                      <div className="flex-1 flex items-center gap-2 min-w-0">
                        <span>{plan.plan_name}</span>
                      </div>
                      {/* 最安値チップ（中央カラム） */}
                      <div className="w-14 flex justify-center items-center">
                        {isCheapest ? (
                          <Badge variant="default" className="bg-orange-500 text-white text-xs whitespace-nowrap h-6 flex items-center justify-center">
                            最安値
                          </Badge>
                        ) : (
                          <div className="h-6" />
                        )}
                      </div>
                      {/* 値段・顧客タイプ */}
                      <div className="text-right min-w-[80px]">
                        <span className={`font-bold ${
                          isCheapest ? 'text-orange-600' : 'text-indigo-600'
                        }`}>
                          ¥{displayPrice.toLocaleString()}
                        </span>
                        <div className="text-xs text-gray-500">{priceType}</div>
                      </div>
                    </div>
                  );
                })}
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
