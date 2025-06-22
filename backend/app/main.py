from datetime import datetime, timedelta
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select
from fastapi import Query
from typing import List
from .db import SessionDep

# from app.dummy_karaoke_stores import dummy_stores
from app.utils import (
    find_cheapest_plan_for_store,
    haversine,
    is_within_time_range,
)

from .db import (
    SessionDep,  # または適切なimportパス
    reset_db_and_tables,
)
from .models import (
    KaraokeStoreDB,
    PlanOptionDB,
)
from .schemas import PlanDetail, SearchRequest, SearchResponse, SearchResultItem, StoreDetailResponse, PriceBreakdown
from .seed import seed_all


@asynccontextmanager
async def lifespan(app: FastAPI):
    reset_db_and_tables()
    seed_all()
    yield


app = FastAPI(lifespan=lifespan)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React側のURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/stores/{store_id}", response_model=StoreDetailResponse)
async def get_store_detail(
    store_id: int,
    session: SessionDep,
    start_time: str = Query(..., description="利用開始時刻（例: '18:00'）"),
):
    """
    指定した店舗ID・利用開始時刻から、その日の営業終了時刻までに一部でも重なる全プラン詳細を返すエンドポイント。
    - 日付をまたぐ営業時間（例: 10:00〜翌5:00）にも対応。
    - 例1: 6/23(月) AM2:00に検索 → 6/23 2:00〜5:00までに利用可能なプランを全て返す
    - 例2: 6/22(日) 16:00に検索 → 6/22 16:00〜6/23 5:00までに利用可能なプランを全て返す
    - プランの時間帯が検索区間（start_time〜営業終了時刻）と一部でも重なっていれば返す
    """
    store = session.get(KaraokeStoreDB, store_id)
    if store is None:
        raise HTTPException(status_code=404, detail="Shop not found")

    today = datetime.now().date()
    start_dt = datetime.strptime(f"{today} {start_time}", "%Y-%m-%d %H:%M")
    day = start_dt.strftime("%a").lower()

    # 閉店時刻を取得（当日のbusiness_hoursから）
    closing_time = None
    for bh in store.business_hours:
        if bh.day_type.value == day:
            closing_time = bh.end_time
            break
    if not closing_time:
        closing_time = "23:59"  # fallback

    # start_dt: 検索開始時刻（datetime）
    # closing_dt: 営業終了時刻（datetime, 日付またぎ対応）
    if closing_time == "24:00":
        closing_time_dt = datetime.strptime("00:00", "%H:%M")
        closing_dt = datetime.combine(start_dt.date(), closing_time_dt.time()) + timedelta(days=1)
    else:
        closing_dt = datetime.combine(start_dt.date(), datetime.strptime(closing_time, "%H:%M").time())
        if closing_time < start_time:  # 例: 10:00〜05:00 の場合
            closing_dt += timedelta(days=1)

    # プランの時間帯が検索区間（start_dt〜closing_dt）と重なるものを返す
    plan_dict = {}
    for plan in store.pricing_plans:
        plan_start_dt = datetime.combine(start_dt.date(), datetime.strptime(plan.start_time, "%H:%M").time())
        plan_end_dt = datetime.combine(start_dt.date(), datetime.strptime(plan.end_time, "%H:%M").time())
        if plan_end_dt <= plan_start_dt:
            plan_end_dt += timedelta(days=1)  # 日付またぎ
        # 区間が重なっていればOK
        latest_start = max(start_dt, plan_start_dt)
        earliest_end = min(closing_dt, plan_end_dt)
        if latest_start < earliest_end:
            if plan.plan_name not in plan_dict:
                plan_dict[plan.plan_name] = {
                    "plan_name": plan.plan_name,
                    "general_price": None,
                    "student_price": None,
                    "member_price": None,
                    "time_range": f"{plan.start_time}~{plan.end_time}",
                }
            for option in plan.options:
                if option.customer_type.value == "general":
                    plan_dict[plan.plan_name]["general_price"] = option.amount
                elif option.customer_type.value == "student":
                    plan_dict[plan.plan_name]["student_price"] = option.amount
                elif option.customer_type.value == "member":
                    plan_dict[plan.plan_name]["member_price"] = option.amount
    plans = [PlanDetail(**v) for v in plan_dict.values()]

    return StoreDetailResponse(
        store_id=store.id, store_name=store.store_name, phone_number=getattr(store, "phone_number", None), plans=plans
    )


def calculate_price_per_30min(option: PlanOptionDB, total_price: int, stay_minutes: int) -> int:
    """
    30分あたりの料金を計算する補助関数
    """
    if option.unit_type.value == "per_30min":
        return option.amount
    elif option.unit_type.value == "per_hour":
        return option.amount // 2
    else:
        # free_time, pack, specialの場合は実際の滞在時間で割る
        return int(total_price * 30 / stay_minutes) if stay_minutes > 0 else 0


def is_member_store(store: KaraokeStoreDB, member_chains: list[str] | None) -> bool:
    """
    指定した店舗が会員店舗かどうか判定する。
    chain_nameがmember_chainsに含まれていればTrue。
    """
    if not member_chains:
        return False
    return store.chain_name in member_chains


@app.post("/search", response_model=SearchResponse)
async def search_shops(request: SearchRequest, session: SessionDep):
    """
    検索条件に合致するカラオケ店舗のリストを返す。並び順は店舗の最安値順。
    """
    results = []
    today = datetime.now().date()
    start_dt = datetime.strptime(f"{today} {request.start_time}", "%Y-%m-%d %H:%M")
    # DBから全店舗を取得
    statement = select(KaraokeStoreDB)
    stores = session.exec(statement).all()
    for store in stores:
        distance = haversine(request.latitude, request.longitude, store.latitude, store.longitude)
        # 指定半径外は除外
        if distance > request.radius:
            continue
        # 会員判定
        is_member = is_member_store(store, getattr(request, "member_chains", None))
        result = find_cheapest_plan_for_store(store, start_dt, request.stay_minutes, is_member, request.is_student)
        if not result:
            continue
        # ドリンクオプション取得
        drink_option = getattr(result["option"], "drink_option", "") if result.get("option") else ""
        # breakdownからtime_rangeを取得（utils.pyで正しいtime_rangeを返すよう修正済み）
        price_breakdown = result["breakdown"] if "breakdown" in result else []
        # breakdownの最初の区間のtime_rangeを使う
        time_range = price_breakdown[0].time_range if price_breakdown else ""
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


@app.get("/hello")
async def hello():
    """
    ヘルスチェック用エンドポイント。
    """
    return {"message": "Hello!"}
