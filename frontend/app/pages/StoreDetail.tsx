import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Sheet, SheetContent } from "@/components/ui/sheet"
import { MapPin, Phone, Star, Navigation } from "lucide-react"
import { Store, MembershipSettings } from "../types/store"
import Image from "next/image"

interface StoreDetailProps {
  store: Store | null
  onClose: () => void
  membershipSettings: MembershipSettings
}

export function StoreDetail({ store, onClose, membershipSettings }: StoreDetailProps) {
  if (!store) return null

  const isMember = membershipSettings[store.chainKey as keyof typeof membershipSettings]?.isMember
  const memberPrice = store.memberPrice
  const regularPrice = store.price

  const chainLogoMap: Record<string, string> = {
    karaokeCan: '/karaokeCan.png',
    bigEcho: '/bigEcho.jpeg',
    tetsuJin: '/karaokeTetsujin.jpeg',
    manekineko: '/manekiNeko.jpg',
    jankara: '/jyanKara.jpg',
    utahiroba: '/utahiroba.jpeg',
  }

  return (
    <Sheet open={!!store} onOpenChange={onClose}>
      <SheetContent side="bottom" className="h-[90vh] rounded-t-xl">
        <div className="py-6 space-y-6">
          {/* Store Header */}
          <div className="text-center">
            <div className="w-16 h-16 rounded-full overflow-hidden flex items-center justify-center mx-auto mb-3 bg-white border">
              <Image
                src={chainLogoMap[store.chainKey] || '/placeholder-logo.png'}
                alt={store.chain}
                width={64}
                height={64}
                className="object-contain w-full h-full"
              />
            </div>
            <h2 className="text-xl font-bold text-gray-900">{store.name}</h2>
            <p className="text-gray-500">{store.address}</p>
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
          </div>

          {/* Features */}
          <div className="space-y-3">
            <h3 className="font-semibold text-gray-900">サービス</h3>
            <div className="flex flex-wrap gap-2">
              {store.features.map((feature) => (
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
  )
} 