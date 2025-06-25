# import pytest
# from datetime import datetime, timedelta
# from app.utils import find_cheapest_plan_for_store
# from app.models import CustomerType, UnitType, KaraokeStoreDB, PricingPlanDB, PlanOptionDB, BusinessHourDB, DayType, TaxType

# def make_store_with_plans():
#     # 10:00-12:00: 30分プラン(300円)
#     # 12:00-18:00: フリータイム(1000円)
#     # 18:00-20:00: 30分プラン(400円)
#     return KaraokeStoreDB(
#         id=1,
#         store_name="テストカラオケ",
#         latitude=0.0,
#         longitude=0.0,
#         phone_number="000-0000-0000",
#         tax_type=TaxType.tax_included,
#         chain_name="テストチェーン",
#         business_hours=[BusinessHourDB(day_type=DayType.sun, start_time="10:00", end_time="20:00")],
#         pricing_plans=[
#             PricingPlanDB(
#                 plan_name="30分プラン午前",
#                 start_time="10:00",
#                 end_time="12:00",
#                 options=[PlanOptionDB(days=["sun"], customer_type=CustomerType.general, amount=300, unit_type=UnitType.per_30min)]
#             ),
#             PricingPlanDB(
#                 plan_name="昼フリータイム",
#                 start_time="12:00",
#                 end_time="18:00",
#                 options=[PlanOptionDB(days=["sun"], customer_type=CustomerType.general, amount=1000, unit_type=UnitType.free_time)]
#             ),
#             PricingPlanDB(
#                 plan_name="30分プラン夜",
#                 start_time="18:00",
#                 end_time="20:00",
#                 options=[PlanOptionDB(days=["sun"], customer_type=CustomerType.general, amount=400, unit_type=UnitType.per_30min)]
#             ),
#         ]
#     )

# def test_free_time_applied():
#     store = make_store_with_plans()
#     dt = datetime(2025, 6, 22, 12, 0)  # 12:00開始（日曜）
#     result = find_cheapest_plan_for_store(store, dt, 180, is_member=False, is_student=False)
#     assert result is not None
#     assert result["total_price"] == 1000  # フリータイムが全体に適用
#     assert len(result["breakdown"]) == 1
#     assert result["breakdown"][0].plan_name == "昼フリータイム"

# def test_plan_switch():
#     store = make_store_with_plans()
#     dt = datetime(2025, 6, 22, 11, 30)  # 11:30開始（日曜）
#     result = find_cheapest_plan_for_store(store, dt, 120, is_member=False, is_student=False)
#     assert result is not None
#     # 11:30-12:00: 30分プラン午前(300円), 12:00-13:00: 昼フリータイム(1000円, break)
#     assert result["total_price"] == 300 + 1000
#     assert len(result["breakdown"]) == 2
#     assert result["breakdown"][0].plan_name == "30分プラン午前"
#     assert result["breakdown"][1].plan_name == "昼フリータイム"

# def test_no_plan():
#     store = make_store_with_plans()
#     dt = datetime(2025, 6, 22, 9, 0)  # 9:00開始（日曜）
#     result = find_cheapest_plan_for_store(store, dt, 60, is_member=False, is_student=False)
#     assert result is None
