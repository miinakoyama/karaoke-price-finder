from datetime import datetime

from backend.app.seed_data import karaoke_stores
from app.utils import find_cheapest_plan_for_store


def test_cheapest_plan_general():
    """
    一般ユーザーで該当プランが見つかるケース。
    - 2025-06-16(月) 12:00開始、90分利用。
    - まねきねこ六本木店の平日昼フリータイム or 30分料金が該当。
    """
    dt = datetime(2025, 6, 16, 12, 0)  # 月曜
    result = find_cheapest_plan_for_store(karaoke_stores[0], dt, 90, is_member=False, is_student=False)
    assert result is not None
    assert result["total_price"] > 0
    assert result["plan_name"] in ["昼フリータイム", "30分料金"]


def test_cheapest_plan_student_weekend():
    """
    学生ユーザーで土日の学割プランが適用されるケース。
    - 2025-06-15(日) 13:00開始、60分利用。
    - まねきねこ六本木店の学生フリータイムが該当。
    """
    dt = datetime(2025, 6, 15, 13, 0)  # 日曜
    result = find_cheapest_plan_for_store(karaoke_stores[0], dt, 60, is_member=False, is_student=True)
    assert result is not None
    assert result["option"].customer_type == "student"
    assert result["total_price"] == 1200


def test_cheapest_plan_member_weekend():
    """
    会員ユーザーで土日の30分料金が適用されるケース。
    - 2025-06-15(日) 10:00開始、60分利用。
    - まねきねこ六本木店の会員30分料金が該当。
    """
    dt = datetime(2025, 6, 15, 10, 0)  # 日曜
    result = find_cheapest_plan_for_store(karaoke_stores[0], dt, 60, is_member=True, is_student=False)
    assert result is not None
    assert result["option"].customer_type == "member"
    assert result["plan_name"] == "30分料金"
    assert result["total_price"] == 273 * 2


def test_cheapest_plan_no_match():
    """
    条件に合致するプランが存在しない場合。
    - 2025-06-18(水) 03:00開始、60分利用。
    - どのプランにも該当しない。
    """
    dt = datetime(2025, 6, 18, 3, 0)  # 水曜深夜
    result = find_cheapest_plan_for_store(karaoke_stores[0], dt, 60, is_member=False, is_student=False)
    assert result is None


def test_cheapest_plan_special_pack():
    """
    スペシャル学割パック（0円）が適用されるケース。
    - 2025-06-14(土) 10:00開始、60分利用。
    - ビッグエコー赤坂駅前店のスペシャル学割パックが該当。
    """
    dt = datetime(2025, 6, 13, 15, 0)  # 金曜、店舗営業時間内に変更
    result = find_cheapest_plan_for_store(karaoke_stores[1], dt, 60, is_member=False, is_student=True)
    assert result is not None
    assert result["plan_name"] == "スペシャル学割パック"
    assert result["option"].unit_type == "special"
    assert result["total_price"] == 0
