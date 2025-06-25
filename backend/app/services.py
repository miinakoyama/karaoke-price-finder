from datetime import datetime, timedelta

from sqlmodel import select

from .db import SessionDep
from .schemas import PlanDetail, SearchRequest, SearchResponse, SearchResultItem, StoreDetailResponse
from .tables import KaraokeStoreDB
from .utils import find_cheapest_plan_for_store, haversine, is_member_store


def get_store_plans(store: KaraokeStoreDB, start_time: str) -> StoreDetailResponse:
    """
    指定した店舗ID・利用開始時刻から、その日の営業終了時刻までに一部でも重なる全プラン詳細を返す。

    Args:
        store (KaraokeStoreDB): 対象店舗のDBモデル
        start_time (str): 利用開始時刻（'HH:MM'形式）
    Returns:
        StoreDetailResponse: 店舗情報と該当プランリスト
    """
    today = datetime.now().date()
    start_dt = datetime.strptime(f"{today} {start_time}", "%Y-%m-%d %H:%M")
    day = start_dt.strftime("%a").lower()

    # 指定日の閉店時刻を取得（なければデフォルト23:59）
    closing_time = next((bh.end_time for bh in store.business_hours if bh.day_type.value == day), "23:59")

    # 営業終了時刻のdatetime計算（日付またぎ対応）
    if closing_time == "24:00":
        closing_dt = datetime.combine(start_dt.date(), datetime.strptime("00:00", "%H:%M").time()) + timedelta(days=1)
    else:
        closing_dt = datetime.combine(start_dt.date(), datetime.strptime(closing_time, "%H:%M").time())
        # 例: 10:00〜05:00 の場合は翌日まで営業
        if closing_time < start_time:
            closing_dt += timedelta(days=1)

    # プランの時間帯が検索区間（start_dt〜closing_dt）と重なるものを抽出
    plan_dict = {}
    for plan in store.pricing_plans:
        plan_start_dt = datetime.combine(start_dt.date(), datetime.strptime(plan.start_time, "%H:%M").time())
        plan_end_dt = datetime.combine(start_dt.date(), datetime.strptime(plan.end_time, "%H:%M").time())
        if plan_end_dt <= plan_start_dt:
            plan_end_dt += timedelta(days=1)  # 日付またぎ
        # 区間が重なっていればOK
        if max(start_dt, plan_start_dt) < min(closing_dt, plan_end_dt):
            plan_info = plan_dict.setdefault(
                plan.plan_name,
                {
                    "plan_name": plan.plan_name,
                    "general_price": None,
                    "student_price": None,
                    "member_price": None,
                    "time_range": f"{plan.start_time}~{plan.end_time}",
                },
            )
            # 各顧客タイプごとの金額を格納
            for option in plan.options:
                if option.customer_type.value == "general":
                    plan_info["general_price"] = option.amount
                elif option.customer_type.value == "student":
                    plan_info["student_price"] = option.amount
                elif option.customer_type.value == "member":
                    plan_info["member_price"] = option.amount
    plans = [PlanDetail(**v) for v in plan_dict.values()]

    return StoreDetailResponse(
        store_id=store.id,
        store_name=store.store_name,
        phone_number=getattr(store, "phone_number", None),
        plans=plans,
    )


def search_karaoke_shops(request: SearchRequest, session: SessionDep) -> SearchResponse:
    """
    検索条件に合致するカラオケ店舗のリストを返す。並び順は店舗の最安値順。

    Args:
        request (SearchRequest): 検索条件
        session (SessionDep): DBセッション依存性
    Returns:
        SearchResponse: 検索結果（店舗リスト）
    """
    today = datetime.now().date()
    start_dt = datetime.strptime(f"{today} {request.start_time}", "%Y-%m-%d %H:%M")
    statement = select(KaraokeStoreDB)
    stores = session.exec(statement).all()
    results = []
    for store in stores:
        # 2点間の距離を計算し、指定半径外は除外
        distance = haversine(request.latitude, request.longitude, store.latitude, store.longitude)
        if distance > request.radius:
            continue
        # 会員判定
        is_member = is_member_store(store, getattr(request, "member_chains", None))
        # 最安プラン検索
        result = find_cheapest_plan_for_store(store, start_dt, request.stay_minutes, is_member, request.is_student)
        if not result:
            continue
        # ドリンクオプションや料金内訳を取得
        drink_option = getattr(result["option"], "drink_option", "") if result.get("option") else ""
        price_breakdown = result.get("breakdown", [])
        # 結果リストに追加
        results.append(
            SearchResultItem(
                store_id=store.id,
                chain_name=store.chain_name,
                store_name=store.store_name,
                lowest_price_per_person=int(result["total_price"]),
                drink_option=drink_option,
                distance=float(distance),
                latitude=store.latitude,
                longitude=store.longitude,
                phone_number=getattr(store, "phone_number", None),
                price_breakdown=price_breakdown,
            )
        )
    # 最安値順にソート
    results.sort(key=lambda x: x.lowest_price_per_person)
    return SearchResponse(results=results)
