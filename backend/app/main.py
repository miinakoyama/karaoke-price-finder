from datetime import datetime
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends,FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.dummy_karaoke_stores import dummy_stores
from app.utils import (
    find_cheapest_plan_for_store,
    is_store_open,
    list_available_plans_for_store,
)

from sqlmodel import Field, Session, SQLModel, create_engine, select, Column, Relationship

from sqlalchemy.types import Enum as SQLEnum
from .schemas import SearchRequest,ShopDetail,SearchResponse,PlanDetail,GetDetailRequest,GetDetailResponse
from .db import create_db_and_tables
from .seed import seed_plan_option_data

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React側のURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    seed_plan_option_data()


@app.post("/get_detail", response_model=GetDetailResponse)
async def get_shop_detail(request: GetDetailRequest):
    """
    指定した店舗ID・利用開始時刻・利用時間・会員/学生区分で、
    条件に合致する全プラン詳細を返すエンドポイント。
    """
    try:
        shop_id = int(request.shop_id)
        store = next((s for s in dummy_stores if s.id == shop_id), None)
        if store is None:
            raise HTTPException(status_code=404, detail="Shop not found")
        today = datetime.now().date()
        start_time_str = request.start_time
        start_dt = datetime.strptime(f"{today} {start_time_str}", "%Y-%m-%d %H:%M")
        stay_minutes = request.stay_minutes or 60
        is_student = request.is_student
        member_shop_ids = request.member_shop_ids or []
        is_member = store.chain_name in member_shop_ids
        plans_data = list_available_plans_for_store(store, start_dt, stay_minutes, is_member, is_student)
        plans = [
            PlanDetail(
                plan_name=plan["plan_name"],
                unit=plan["unit"],
                price=plan["price"],
                price_per_30_min=plan["price_per_30_min"],
                start=plan["start"],
                end=plan["end"],
                customer_type=plan["customer_type"],
            )
            for plan in plans_data
        ]
        return GetDetailResponse(shop_id=str(store.id), name=store.store_name, plans=plans)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shop_id format")
    except Exception as e:
        print(f"Error in get_shop_detail: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/search", response_model=SearchResponse)
async def search_shops(request: SearchRequest):
    """
    検索条件に合致するカラオケ店舗の最安値プランを返すエンドポイント。
    - 店舗ごとに最安値プランを1件返す
    - 店舗情報・最安値・プラン名などを含む
    - 緯度・経度・半径が指定されていれば、その範囲内の店舗のみ対象
    """
    results = []
    today = datetime.now().date()
    start_time_str = request.start_time
    start_dt = datetime.strptime(f"{today} {start_time_str}", "%Y-%m-%d %H:%M")
    stay_minutes = request.stay_minutes or 60
    is_student = request.is_student
    member_shop_ids = request.member_shop_ids or []
    latitude = getattr(request, "latitude", None)
    longitude = getattr(request, "longitude", None)
    radius = getattr(request, "radius", None)
    filtered_stores = dummy_stores
    if latitude is not None and longitude is not None and radius is not None:
        from app.utils import haversine

        filtered_stores = [
            s for s in dummy_stores if haversine(latitude, longitude, s.latitude, s.longitude) <= radius
        ]
    for store in filtered_stores:
        is_member = store.chain_name in member_shop_ids
        result = find_cheapest_plan_for_store(store, start_dt, stay_minutes, is_member, is_student)
        if not result:
            continue
        # 距離計算
        distance = None
        if latitude is not None and longitude is not None and store.latitude is not None and store.longitude is not None:
            from app.utils import haversine

            distance = haversine(latitude, longitude, store.latitude, store.longitude)
        shop_detail = ShopDetail(
            shop_id=str(store.id),
            name=store.store_name,
            price_per_person=int(result["total_price"]),
            icon_url=store.chain_name,
            drink_type=", ".join(result["drink_type"]) if result["drink_type"] else None,  # リストを文字列に変換
            phone=store.phone_number,
            all_plans=[result["plan_name"]],
            latitude=store.latitude,
            longitude=store.longitude,
            distance=distance,
        )
        results.append(shop_detail)
    return SearchResponse(results=results)

# is_store_open関数のテスト用
@app.get("/store/{store_id}/is_open")
def check_store_open_status(
    store_id: int, dt: Annotated[datetime, Query(description="チェックしたい日時（例: 2025-06-20T01:00:00）")] = ...
):
    # 対象店舗を探す
    store = next((s for s in dummy_stores if s.id == store_id), None)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    is_open = is_store_open(store, dt)

    return {"store_id": store.id, "store_name": store.store_name, "datetime": dt.isoformat(), "is_open": is_open}


@app.get("/hello")
async def hello():
    """
    ヘルスチェック用エンドポイント。
    """
    return {"message": "Hello!"}
