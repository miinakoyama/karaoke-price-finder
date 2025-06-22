from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from .models import CustomerType, DayType, KaraokeStoreDB, PricingPlanDB


def get_store_from_db(session: Session, shop_id: int) -> Optional[KaraokeStoreDB]:
    return (
        session.query(KaraokeStoreDB)
        .options(
            selectinload(KaraokeStoreDB.business_hours),
            selectinload(KaraokeStoreDB.pricing_plans).selectinload(PricingPlanDB.options),
        )
        .filter(KaraokeStoreDB.id == shop_id)
        .first()
    )


# データベースから店舗情報を取得する関数
# def get_store_from_db(session: SessionDep, shop_id: int):
#     """データベースから店舗情報を取得"""
#     # KaraokeStoreDBテーブルから店舗情報を取得
#     # statement = select(KaraokeStoreDB).where(KaraokeStoreDB.id == shop_id)
#     with Session(engine) as session:
#         statement = session.get(KaraokeStoreDB,shop_id)
#     # store = session.exec(statement).first()
#     return statement


# 店舗とその関連データを取得する関数
def get_store_with_relations(session: Session, store_id: int) -> Optional[KaraokeStoreDB]:
    """
    店舗IDから店舗とその関連データ（営業時間、プラン、オプション）を取得
    """
    # 店舗を取得（関連データは自動的にロードされる）
    statement = select(KaraokeStoreDB).where(KaraokeStoreDB.id == store_id)
    store = session.exec(statement).first()

    if store:
        # リレーションシップにより関連データにアクセス可能
        # store.business_hours - 営業時間リスト
        # store.pricing_plans - プランリスト
        # store.pricing_plans[i].options - 各プランのオプションリスト
        pass

    return store


# 営業時間チェック用のヘルパー関数
def is_store_open(store: KaraokeStoreDB, check_time: datetime) -> bool:
    """
    指定時刻に店舗が営業しているかチェック
    """
    # 曜日を取得（月曜=0, 日曜=6）
    weekday = check_time.weekday()

    # 営業時間をチェック
    for hours in store.business_hours:
        # DayTypeに応じた営業時間判定ロジック
        # 実際のDayType Enumの実装に合わせて調整してください
        if is_matching_day_type(hours.day_type, weekday):
            start_time = datetime.strptime(hours.start_time, "%H:%M").time()
            end_time = datetime.strptime(hours.end_time, "%H:%M").time()
            current_time = check_time.time()

            # 終了時間が翌日にまたがる場合の処理
            if end_time < start_time:  # 例: 10:00-26:00 (翌日2:00)
                if current_time >= start_time or current_time <= end_time:
                    return True
            else:
                if start_time <= current_time <= end_time:
                    return True

    return False


def is_matching_day_type(day_type: DayType, weekday: int) -> bool:
    """
    DayTypeと曜日が一致するかチェック
    """
    # 実際のDayType Enumの実装に合わせて調整してください
    if day_type == DayType.WEEKDAY:
        return weekday < 5  # 月-金
    elif day_type == DayType.WEEKEND:
        return weekday >= 5  # 土-日
    # その他の条件...
    return False


# 適用可能な料金プランを取得
def get_applicable_pricing_plans(store: KaraokeStoreDB, start_time: datetime, is_student: bool) -> List[PricingPlanDB]:
    """
    指定時刻と顧客タイプに適用可能な料金プランを取得
    """
    applicable_plans = []

    for plan in store.pricing_plans:
        plan_start = datetime.strptime(plan.start_time, "%H:%M").time()
        plan_end = datetime.strptime(plan.end_time, "%H:%M").time()
        current_time = start_time.time()

        # 時間帯チェック
        time_matches = False
        if plan_end < plan_start:  # 翌日にまたがる場合
            time_matches = current_time >= plan_start or current_time <= plan_end
        else:
            time_matches = plan_start <= current_time <= plan_end

        if time_matches:
            # このプランに適用可能なオプションがあるかチェック
            for option in plan.options:
                customer_matches = (is_student and option.customer_type == CustomerType.STUDENT) or (
                    not is_student and option.customer_type == CustomerType.ADULT
                )

                if customer_matches:
                    applicable_plans.append(plan)
                    break  # このプランは適用可能

    return applicable_plans
