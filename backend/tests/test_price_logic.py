"""
料金計算ロジック（find_cheapest_plan_for_store）の最低限テスト。
- フリータイム適用の正常系
- プラン切替時のbreakdown分割・合計金額
- 該当プランなし
"""

from datetime import datetime

from app.tables import (
    BusinessHourDB,
    CustomerType,
    DayType,
    KaraokeStoreDB,
    PlanOptionDB,
    PricingPlanDB,
    TaxType,
    UnitType,
)
from app.utils import find_cheapest_plan_for_store


def make_store_with_plans():
    """
    テスト用のカラオケ店舗データを生成。
    - 10:00-12:00: 30分プラン(300円)
    - 12:00-18:00: フリータイム(1000円)
    - 18:00-20:00: 30分プラン(400円)
    """
    return KaraokeStoreDB(
        id=1,
        store_name="テストカラオケ",
        latitude=0.0,
        longitude=0.0,
        phone_number="000-0000-0000",
        tax_type=TaxType.tax_included,
        chain_name="テストチェーン",
        business_hours=[BusinessHourDB(day_type=DayType.sun, start_time="10:00", end_time="20:00")],
        pricing_plans=[
            PricingPlanDB(
                plan_name="30分プラン午前",
                start_time="10:00",
                end_time="12:00",
                options=[
                    PlanOptionDB(
                        days=["sun"], customer_type=CustomerType.general, amount=300, unit_type=UnitType.per_30min
                    )
                ],
            ),
            PricingPlanDB(
                plan_name="昼フリータイム",
                start_time="12:00",
                end_time="18:00",
                options=[
                    PlanOptionDB(
                        days=["sun"], customer_type=CustomerType.general, amount=1000, unit_type=UnitType.free_time
                    )
                ],
            ),
            PricingPlanDB(
                plan_name="30分プラン夜",
                start_time="18:00",
                end_time="20:00",
                options=[
                    PlanOptionDB(
                        days=["sun"], customer_type=CustomerType.general, amount=400, unit_type=UnitType.per_30min
                    )
                ],
            ),
        ],
    )


def test_free_time_applied():
    """
    滞在全体にフリータイムが適用されるケース。
    - 12:00開始、180分滞在（日曜）
    - 昼フリータイム(1000円)のみで計算されること
    """
    store = make_store_with_plans()
    dt = datetime(2025, 6, 22, 12, 0)
    result = find_cheapest_plan_for_store(store, dt, 180, is_member=False, is_student=False)
    assert result is not None
    assert result["total_price"] == 1000
    assert len(result["breakdown"]) == 1
    assert result["breakdown"][0].plan_name == "昼フリータイム"


def test_plan_switch():
    """
    滞在中にプランが切り替わるケース。
    - 11:30開始、120分滞在（日曜）
    - 11:30-12:00: 30分プラン午前(300円)×1
    - 12:00-13:00: 昼フリータイム(1000円)×3（30分ごとにbreakdownされる仕様）
    - 合計3300円、breakdownが4件
    ※現状ロジックでは30分ごとにbreakdownが分割される
    """
    store = make_store_with_plans()
    dt = datetime(2025, 6, 22, 11, 30)
    result = find_cheapest_plan_for_store(store, dt, 120, is_member=False, is_student=False)
    assert result is not None
    assert result["total_price"] == 3300
    assert len(result["breakdown"]) == 4
    assert result["breakdown"][0].plan_name == "30分プラン午前"
    assert all(b.plan_name == "昼フリータイム" for b in result["breakdown"][1:])


def test_no_plan():
    """
    該当するプランが存在しないケース。
    - 9:00開始、60分滞在（日曜）
    - どのプランにも該当せず、Noneが返る
    """
    store = make_store_with_plans()
    dt = datetime(2025, 6, 22, 9, 0)
    result = find_cheapest_plan_for_store(store, dt, 60, is_member=False, is_student=False)
    assert result is None
