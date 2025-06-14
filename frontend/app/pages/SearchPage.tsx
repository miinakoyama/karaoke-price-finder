import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import { Slider } from "@/components/ui/slider"
import { Badge } from "@/components/ui/badge"
import { MapPin, Search, Clock, Users, ChevronDown, Menu } from "lucide-react"
import { SettingsSheet } from "./SettingsSheet"
import { MembershipSettings } from "../types/store"
import { useState } from "react"

interface SearchPageProps {
  searchLocation: string
  setSearchLocation: (location: string) => void
  duration: number[]
  setDuration: (duration: number[]) => void
  people: number
  setPeople: (people: number) => void
  studentDiscount: boolean
  setStudentDiscount: (discount: boolean) => void
  drinkBar: boolean
  setDrinkBar: (drinkBar: boolean) => void
  onSearch: () => void
  onUseCurrentLocation: () => void
  membershipSettings: MembershipSettings
  updateMembership: (chainKey: string, isMember: boolean, memberNumber?: string) => void
}

export function SearchPage({
  searchLocation,
  setSearchLocation,
  duration,
  setDuration,
  people,
  setPeople,
  studentDiscount,
  setStudentDiscount,
  drinkBar,
  setDrinkBar,
  onSearch,
  onUseCurrentLocation,
  membershipSettings,
  updateMembership,
}: SearchPageProps) {
  const [drawerOpen, setDrawerOpen] = useState(false)

  const formatDuration = (hours: number) => {
    const h = Math.floor(hours)
    const m = Math.round((hours - h) * 60)
    if (h === 0) return `${m}分`
    if (m === 0) return `${h}時間`
    return `${h}時間${m}分`
  }

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
        <SettingsSheet
          open={drawerOpen}
          onOpenChange={setDrawerOpen}
          membershipSettings={membershipSettings}
          updateMembership={updateMembership}
          people={people}
          setPeople={setPeople}
          drinkBar={drinkBar}
          setDrinkBar={setDrinkBar}
        />
      </header>

      {/* Search Card */}
      <div className="p-4">
        <Card className="shadow-sm">
          <CardContent className="p-4 space-y-4">
            {/* Location */}
            <div className="space-y-2">
              <Button variant="outline" className="w-full justify-start gap-2" onClick={onUseCurrentLocation}>
                <MapPin className="w-4 h-4" />
                現在地を使う
              </Button>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <Input
                  placeholder="住所を入力"
                  className="pl-10"
                  value={searchLocation}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSearchLocation(e.target.value)}
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
                  <Slider value={duration} onValueChange={setDuration} max={8} min={0.5} step={0.5} className="w-full" />
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
            <Button className="w-full bg-orange-500 hover:bg-orange-600" onClick={onSearch}>
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