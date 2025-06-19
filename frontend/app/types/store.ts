export interface Store {
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
  latitude: number
  longitude: number
}

export interface MembershipSettings {
  karaokeCan: { isMember: boolean }
  bigEcho: { isMember: boolean }
  tetsuJin: { isMember: boolean }
  manekineko: { isMember: boolean }
  jankara: { isMember: boolean }
  utahiroba: { isMember: boolean }
}

export const mockStores: Store[] = [
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
    features: ["ドリンクバー付"],
    chainKey: "karaokeCan",
    latitude: 35.6595,
    longitude: 139.7005,
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
    features: [],
    chainKey: "bigEcho",
    latitude: 35.6745,
    longitude: 139.7366,
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
    features: ["ドリンクバー付"],
    chainKey: "tetsuJin",
    latitude: 35.6618,
    longitude: 139.7353,
  },
]
