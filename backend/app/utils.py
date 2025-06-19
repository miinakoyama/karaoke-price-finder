from datetime import datetime, time
import math
from app.models import KaraokeStore
from math import radians, cos, sin, asin, sqrt


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
    指定時刻dtがstart_str〜end_strの範囲内か判定する（24時跨ぎ対応）。

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

    if start < end:
        return start <= target_time < end
    else:
        return target_time >= start or target_time < end


def find_cheapest_plan_for_store(store: KaraokeStore, dt: datetime, stay_minutes: int, is_member: bool, is_student: bool):
    """
    指定したカラオケ店舗・日時・利用時間・会員/学生区分で最安値プランを計算する。

    Args:
        store (KaraokeStore): 対象のカラオケ店舗インスタンス
        dt (datetime): 利用開始日時
        stay_minutes (int): 利用時間（分）
        is_member (bool): 会員かどうか
        is_student (bool): 学生かどうか

    Returns:
        dict or None: 最安値プランが見つかった場合は{
            'plan_name': str,
            'option': PlanOption,
            'total_price': int
        }を返す。該当プランがなければNone。
    """
    day = get_weekday_str(dt)
    best_price = float('inf')
    best_plan = None
    best_option = None

    types_to_check = []
    if is_member:
        types_to_check.append("member")
    if is_student:
        types_to_check.append("student")
    if not types_to_check:
        types_to_check.append("general")

    for plan in store.pricing_plans:
        # 時間帯が合うか
        if not is_within_time_range(plan.start_time, plan.end_time, dt):
            continue
        for option in plan.options:
            # 曜日・顧客種別が合うか
            if day not in option.days:
                continue
            if option.customer_type not in types_to_check:
                continue
            # 金額計算
            if option.unit_type == "per_30min":
                units = math.ceil(stay_minutes / 30)
                total = option.amount * units
            elif option.unit_type == "per_hour":
                units = math.ceil(stay_minutes / 60)
                total = option.amount * units
            elif option.unit_type in ("free_time", "pack", "special"):
                total = option.amount
            else:
                continue
            if total < best_price:
                best_price = total
                best_plan = plan
                best_option = option
    if best_plan and best_option:
        return {
            "plan_name": best_plan.plan_name,
            "option": best_option,
            "total_price": best_price
        }
    else:
        return None


def list_available_plans_for_store(store: KaraokeStore, dt: datetime, stay_minutes: int, is_member: bool, is_student: bool):
    """
    指定したカラオケ店舗・日時・利用時間・会員/学生区分で該当する全プラン（PlanDetail相当の情報）をリストで返す。

    Args:
        store (KaraokeStore): 対象のカラオケ店舗インスタンス
        dt (datetime): 利用開始日時
        stay_minutes (int): 利用時間（分）
        is_member (bool): 会員かどうか
        is_student (bool): 学生かどうか
    Returns:
        list: 条件に合致するプラン情報のリスト
    """
    plans = []
    day = get_weekday_str(dt)
    for plan in store.pricing_plans:
        if not is_within_time_range(plan.start_time, plan.end_time, dt):
            continue
        for option in plan.options:
            if day not in option.days:
                continue
            # customer_type判定
            if is_member and option.customer_type == "member":
                pass
            elif is_student and option.customer_type == "student":
                pass
            elif option.customer_type == "general":
                pass
            else:
                continue
            # 金額計算
            if option.unit_type == "per_30min":
                units = math.ceil(stay_minutes / 30)
                total = option.amount * units
            elif option.unit_type == "per_hour":
                units = math.ceil(stay_minutes / 60)
                total = option.amount * units
            else:
                total = option.amount
            plans.append({
                "unit": option.unit_type,
                "price": int(total),
                "price_per_30_min": option.amount if option.unit_type == "per_30min" else None,
                "start": plan.start_time,
                "end": plan.end_time,
                "customer_type": [option.customer_type]
            })
    return plans


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
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c
