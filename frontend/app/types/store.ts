import { PlanCalc } from './api'

export interface Store {
  shop_id: string
  name: string
  icon_url: string
  price_per_person: number
  memberPrice?: number
  drinkInfo: string
  badges: string[]
  distance: string
  rating: number
  address: string
  phone: string
  features: string[]
  all_plans: string[]
  chainKey: string
  latitude: number
  longitude: number
  plan_calc?: PlanCalc[]
}

export interface MembershipSettings {
  karaokeCan: { isMember: boolean }
  bigEcho: { isMember: boolean }
  tetsuJin: { isMember: boolean }
  manekineko: { isMember: boolean }
  jankara: { isMember: boolean }
  utahiroba: { isMember: boolean }
  pasela: { isMember: boolean }
}

export const mockStores: Store[] = [
  {
    shop_id: "1",
    name: "カラオケ館 渋谷本店",
    icon_url: "カラオケ館",
    price_per_person: 1280,
    memberPrice: 1080,
    drinkInfo: "1ドリンク付",
    badges: ["最安", "学割OK"],
    distance: "0.3km",
    rating: 4.2,
    address: "東京都渋谷区道玄坂2-10-7",
    phone: "03-1234-5678",
    features: ["ドリンクバー付"],
    all_plans: ["30分", "2時間パック", "フリータイム", "深夜パック"],
    chainKey: "karaokeCan",
    latitude: 35.6595,
    longitude: 139.7005,
  },
  {
    shop_id: "2",
    name: "ビッグエコー 新宿東口店",
    icon_url: "ビッグエコー",
    price_per_person: 1480,
    memberPrice: 1280,
    drinkInfo: "ワンドリンク必須",
    badges: ["学割OK"],
    distance: "0.5km",
    rating: 4.0,
    address: "東京都新宿区新宿3-15-8",
    phone: "03-2345-6789",
    features: [],
    all_plans: ["30分", "2時間パック", "フリータイム", "深夜パック"],
    chainKey: "bigEcho",
    latitude: 35.6745,
    longitude: 139.7366,
  },
  {
    shop_id: "3",
    name: "カラオケの鉄人 池袋店",
    icon_url: "カラオケの鉄人",
    price_per_person: 1680,
    memberPrice: 1480,
    drinkInfo: "ドリンクバー付",
    badges: ["ドリンクバー付"],
    distance: "0.8km",
    rating: 4.5,
    address: "東京都豊島区南池袋1-20-1",
    phone: "03-3456-7890",
    features: ["ドリンクバー付"],
    all_plans: ["30分", "2時間パック", "フリータイム", "深夜パック"],
    chainKey: "tetsuJin",
    latitude: 35.6618,
    longitude: 139.7353,
  },
]
