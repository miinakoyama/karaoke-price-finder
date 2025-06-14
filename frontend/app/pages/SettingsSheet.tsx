import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { Menu } from "lucide-react"
import { MembershipSettings } from "../types/store"

interface SettingsSheetProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  membershipSettings: MembershipSettings
  updateMembership: (chainKey: string, isMember: boolean, memberNumber?: string) => void
  people: number
  setPeople: (people: number) => void
  drinkBar: boolean
  setDrinkBar: (drinkBar: boolean) => void
}

export function SettingsSheet({
  open,
  onOpenChange,
  membershipSettings,
  updateMembership,
  people,
  setPeople,
  drinkBar,
  setDrinkBar,
}: SettingsSheetProps) {
  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
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
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                      updateMembership("karaokeCan", true, e.target.value)
                    }
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
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                      updateMembership("bigEcho", true, e.target.value)
                    }
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
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                      updateMembership("tetsuJin", true, e.target.value)
                    }
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
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                      updateMembership("manekineko", true, e.target.value)
                    }
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
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                      updateMembership("jankara", true, e.target.value)
                    }
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
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                      updateMembership("utahiroba", true, e.target.value)
                    }
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
                <Button variant={drinkBar ? "default" : "outline"} size="sm" onClick={() => setDrinkBar(!drinkBar)}>
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
  )
} 