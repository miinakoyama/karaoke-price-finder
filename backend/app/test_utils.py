import pytest
from datetime import datetime
from utils import find_cheapest_plan, stores

def test_find_cheapest_plan_general():
    """
    一般ユーザーで該当プランが見つかるケース。
    - 2025-06-17 10:00開始、180分利用。
    - プランが見つかり、種別が正しく、価格が0より大きいこと。
    """
    dt = datetime.fromisoformat("2025-06-17T10:00:00+16:30")
    plan_type, price, ok = find_cheapest_plan(stores[0].rules, dt, "general", 180)
    assert ok
    assert plan_type in ["free_time", "per_30_min"]
    assert price is not None and price > 0

def test_find_cheapest_plan_member():
    """
    会員ユーザーで該当プランが見つかるケース。
    - 2025-06-14 12:00開始、60分利用。
    - プランが見つかり、種別が正しく、価格が0より大きいこと。
    """
    dt = datetime.fromisoformat("2025-06-14T12:00:00+09:00")
    plan_type, price, ok = find_cheapest_plan(stores[0].rules, dt, "member", 60)
    assert ok
    assert plan_type in ["free_time", "per_30_min"]
    assert price is not None and price > 0

def test_find_cheapest_plan_student_fallback():
    """
    学生ユーザーで、一般プランもfallbackで検索されるケース。
    - 2025-06-16 15:00開始、120分利用。
    - プランが見つかり、種別が正しく、価格が0より大きいこと。
    """
    dt = datetime.fromisoformat("2025-06-16T15:00:00+09:00")
    plan_type, price, ok = find_cheapest_plan(stores[0].rules, dt, "student", 120)
    assert ok
    assert plan_type in ["free_time", "per_30_min"]
    assert price is not None and price > 0

def test_find_cheapest_plan_no_plan():
    """
    存在しないユーザー種別で該当プランが見つからないケース。
    - 2025-06-18 03:00開始、unknownユーザー、60分利用。
    - プランが見つからないこと。
    """
    dt = datetime.fromisoformat("2025-06-18T03:00:00+09:00")
    plan_type, price, ok = find_cheapest_plan(stores[0].rules, dt, "unknown", 60)
    assert not ok

def test_find_cheapest_plan_cross_day():
    """
    日付をまたいで利用するケース。
    - 2025-06-14 23:30開始、90分利用（翌日をまたぐ）。
    - プランが見つかり、種別が正しく、価格が0より大きいこと。
    """
    dt = datetime.fromisoformat("2025-06-14T23:30:00+09:00")
    plan_type, price, ok = find_cheapest_plan(stores[0].rules, dt, "general", 90)
    assert ok
    assert plan_type in ["free_time", "per_30_min"]
    assert price is not None and price > 0
