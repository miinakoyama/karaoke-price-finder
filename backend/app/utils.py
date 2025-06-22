import math
from datetime import datetime, time, timedelta
from math import asin, cos, radians, sin, sqrt

from app.models import (
    CustomerType,
    KaraokeStoreDB,
    UnitType,
)


def is_store_open(store: KaraokeStoreDB, dt: datetime) -> bool:
    """
    営業中かどうかを判定する関数
    """
    current_day = get_weekday_str(dt)
    prev_day = get_weekday_str(dt - timedelta(days=1))
    time_str = dt.strftime("%H:%M")
    for bh in store.business_hours:
        # 1.
        if bh.day_type.value == current_day and bh.start_time <= bh.end_time:
            if bh.start_time <= time_str < bh.end_time:
                return True
        # 2. 深夜営業（終了が翌日）
        elif bh.day_type.value == current_day and bh.start_time > bh.end_time:
            if time_str >= bh.start_time or time_str < bh.end_time:
                return True
        # 3. 翌日早朝のカバー（前日の深夜営業）
        elif bh.day_type.value == prev_day and bh.start_time > bh.end_time:
            if time_str < bh.end_time:
                return True

    return False


def get_weekday_str(dt: datetime) -> str:
    """
    指定したdatetimeから曜日を英小文字3文字（例: 'mon', 'tue'）で返す。

    Args:
        dt (datetime): 日時
    Returns:
        str: 曜日（'mon'〜'sun'）
    """
    return dt.strftime("%a").lower()  # e.g., 'mon', 'tue', etc.


def parse_time_str(s: str) -> time:
    """
    'HH:MM'形式の文字列をtime型に変換する。

    Args:
        s (str): 'HH:MM'形式の文字列
    Returns:
        time: 対応するtimeオブジェクト
    """
    return datetime.strptime(s, "%H:%M").time()


def is_within_time_range(start_str: str, end_str: str, dt: datetime) -> bool:
    """
    指定時刻dtがstart_str〜end_strの範囲内か判定する（24時跨ぎ・24時間営業対応）。

    Args:
        start_str (str): 開始時刻（'HH:MM'）
        end_str (str): 終了時刻（'HH:MM'）
        dt (datetime): 判定対象の日時
    Returns:
        bool: 範囲内ならTrue
    """
    start = parse_time_str(start_str)
    end = parse_time_str(end_str)
    target_time = dt.time()

    # 24時間営業（00:00〜24:00 or 00:00〜00:00）は常にTrue
    if start_str == "00:00" and (end_str == "24:00" or end_str == "00:00"):
        return True
    # 24:00は翌日0:00とみなす
    if end_str == "24:00":
        end = time(0, 0)
        if start == end:
            return True  # 00:00〜24:00は常にTrue
    if start < end:
        return start <= target_time < end
    else:
        # 日付またぎ
        return target_time >= start or target_time < end


def find_cheapest_plan_for_store(
    store: KaraokeStoreDB, dt: datetime, stay_minutes: int, is_member: bool, is_student: bool
):
    """
    指定したカラオケ店舗・日時・利用時間・会員/学生区分で、
    区間ごとに最安プランを選び、合計金額と適用プランリストを返す。

    ロジック概要:
    1. 指定日時が店舗の営業時間内かどうかを判定。
    2. 会員/学生区分に応じて適用可能なCustomerTypeを決定。
    3. まず、フリータイム・パック・スペシャルプラン（例: フリータイムやパック）が、
       利用開始時刻と終了時刻の両方ともプランの適用時間帯に含まれていれば、
       そのプランを全体に一括適用し、最安のものを返す。
    4. 上記で全体をカバーできない場合は、利用時間を30分ごとに区切り、
       各区間ごとに利用可能なプランの中から最安のものを選んで適用し、
       合計金額と区間ごとの内訳リストを返す。
       このとき、フリータイム・パック・スペシャルも区間ごとに候補に含めるため、
       時間帯によって料金が異なるフリータイムにも対応できる。
    5. いずれの区間にも該当プランがない場合はNoneを返す。

    例:
      - 19:00〜21:00の利用で、18:00〜22:00のフリータイムがあれば全体に適用。
      - フリータイムで全体をカバーできない場合や、時間帯ごとに料金が異なる場合は、
        19:00〜19:30, 19:30〜20:00...のように30分ごとに最安プランを選び、
        その区間ごとに異なるフリータイム料金も正しく反映される。

    Args:
        store (KaraokeStoreDB): 対象店舗
        dt (datetime): 利用開始日時
        stay_minutes (int): 利用時間（分）
        is_member (bool): 会員かどうか
        is_student (bool): 学生かどうか
    Returns:
        dict or None: {'plan_name', 'option', 'total_price', 'breakdown'} または None（該当プランなし）
    """
    # 1. 営業時間内かどうか判定
    if not is_store_open(store, dt):
        return None
    day = get_weekday_str(dt)
    types_to_check = []
    if is_member:
        types_to_check.append(CustomerType.member)
    if is_student:
        types_to_check.append(CustomerType.student)
    if not types_to_check:
        types_to_check.append(CustomerType.general)

    # 2. フリータイム・パック・スペシャルで全体カバーできるか判定
    from app.schemas import PriceBreakdown

    dt_end = dt + timedelta(minutes=stay_minutes - 1)
    for plan in store.pricing_plans:
        for option in plan.options:
            if option.customer_type not in types_to_check:
                continue
            if day not in option.days:
                continue
            # フリータイム・パック・スペシャルは全体が時間帯に含まれる場合のみ一括適用
            if option.unit_type in (UnitType.free_time, UnitType.pack, UnitType.special):
                if is_within_time_range(plan.start_time, plan.end_time, dt) and is_within_time_range(
                    plan.start_time, plan.end_time, dt_end
                ):
                    breakdown = [
                        PriceBreakdown(
                            plan_name=plan.plan_name,
                            time_range=f"{plan.start_time}~{plan.end_time}",
                            total_price=option.amount,
                        )
                    ]
                    return {
                        "plan_name": plan.plan_name,
                        "option": option,
                        "total_price": option.amount,
                        "breakdown": breakdown,
                    }
    # 3. 30分単位で区間ごとに最安プランを選択（フリータイムも区間ごとに候補に含める）
    intervals = []
    interval_minutes = 30
    num_intervals = math.ceil(stay_minutes / interval_minutes)
    for i in range(num_intervals):
        interval_start = dt + timedelta(minutes=i * interval_minutes)
        interval_end = interval_start + timedelta(minutes=interval_minutes)
        intervals.append((interval_start, interval_end))

    breakdown = []
    total_price = 0
    for interval_start, interval_end in intervals:
        best_price = float("inf")
        best_plan = None
        best_option = None
        # 各区間で利用可能な最安プランを探索（フリータイムも含める）
        for plan in store.pricing_plans:
            if not is_within_time_range(plan.start_time, plan.end_time, interval_start):
                continue
            for option in plan.options:
                if day not in option.days:
                    continue
                if option.customer_type not in types_to_check:
                    continue
                # 30分単位 or 1時間単位 or フリータイム or パック or スペシャルの金額を計算
                if option.unit_type == UnitType.per_30min:
                    price = option.amount
                elif option.unit_type == UnitType.per_hour:
                    price = option.amount // 2
                elif option.unit_type in (UnitType.free_time, UnitType.pack, UnitType.special):
                    price = option.amount
                else:
                    continue
                if price < best_price:
                    best_price = price
                    best_plan = plan
                    best_option = option
        if best_plan and best_option:
            # best_plan.start_time, best_plan.end_timeを直接str変換して結合
            start_str = str(best_plan.start_time)
            end_str = str(best_plan.end_time)
            breakdown.append(
                PriceBreakdown(
                    plan_name=best_plan.plan_name, time_range=start_str + "~" + end_str, total_price=int(best_price)
                )
            )
            total_price += best_price
        else:
            # 該当プランがない区間があれば除外（Noneを返す）
            return None
    return {
        "plan_name": breakdown[0].plan_name if breakdown else None,
        "option": None,
        "total_price": total_price,
        "breakdown": breakdown,
    }


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    2点間の緯度経度から距離（メートル）を返す。

    Args:
        lat1 (float): 1点目の緯度
        lon1 (float): 1点目の経度
        lat2 (float): 2点目の緯度
        lon2 (float): 2点目の経度
    Returns:
        float: 2点間の距離（メートル）
    Raises:
        ValueError: 緯度経度がfloatでない場合
    """
    if not all(isinstance(x, (float, int)) for x in [lat1, lon1, lat2, lon2]):
        raise ValueError("All coordinates must be float or int.")
    R = 6371000  # 地球半径[m]
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c
