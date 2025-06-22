from datetime import datetime
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
)

from .db import (
    SessionDep,  # または適切なimportパス
    reset_db_and_tables,
)
from .models import (
    KaraokeStoreDB,
    PlanOptionDB,
)
from .schemas import PlanDetail, SearchRequest, SearchResponse, SearchResultItem, StoreDetailResponse
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
    指定した店舗ID・利用開始時刻から閉店までの全プラン詳細を返すエンドポイント。
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

    # プランの開始時刻がstart_time以降、かつ終了時刻が閉店時刻以下のものを返す
    plan_dict = {}
    for plan in store.pricing_plans:
        if plan.start_time >= start_time and plan.end_time <= closing_time:
            if plan.plan_name not in plan_dict:
                plan_dict[plan.plan_name] = {
                    "plan_name": plan.plan_name,
                    "general_price": None,
                    "student_price": None,
                    "member_price": None
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
        store_id=store.id,
        store_name=store.store_name,
        phone_number=getattr(store, "phone_number", None),
        plans=plans
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
        from app.utils import haversine

        distance = haversine(request.latitude, request.longitude, store.latitude, store.longitude)
        # 指定半径外は除外
        if distance > request.radius:
            continue
        # 会員判定
        is_member = is_member_store(store, getattr(request, 'member_chains', None))
        result = find_cheapest_plan_for_store(store, start_dt, request.stay_minutes, is_member, request.is_student)
        if not result:
            continue
        # ドリンクオプション取得
        drink_option = getattr(result["option"], "drink_option", "") if result.get("option") else ""
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
