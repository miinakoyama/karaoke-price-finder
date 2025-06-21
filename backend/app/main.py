from datetime import datetime
from typing import List, Optional
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends,FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import selectinload
from .models import CustomerType,DayType,TaxType,UnitType,PlanOptionDB,PricingPlanDB,BusinessHourDB,KaraokeStoreDB
from .db import SessionDep  # または適切なimportパス
# from app.dummy_karaoke_stores import dummy_stores
from app.utils import (
    find_cheapest_plan_for_store,
    is_store_open,
    find_cheapest_plan_for_store,
)

from sqlmodel import Field, Session, SQLModel, create_engine, select, Column, Relationship

from sqlalchemy.types import Enum as SQLEnum
from .schemas import SearchRequest,ShopDetail,SearchResponse,PlanDetail,GetDetailRequest,GetDetailResponse
from .db import create_db_and_tables
from .seed import seed_plan_option_data
from .get_data import get_store_from_db
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
async def get_shop_detail(request: GetDetailRequest, session: SessionDep):
    """
    指定した店舗ID・利用開始時刻・利用時間・会員/学生区分で、
    条件に合致する全プラン詳細を返すエンドポイント。
    """
    try:
        shop_id = int(request.shop_id)
        
        # Dependency Injectionで受け取ったセッションを使用
        store = session.get(KaraokeStoreDB, shop_id)
        if store is None:
            raise HTTPException(status_code=404, detail="Shop not found")
            
        today = datetime.now().date()
        start_time_str = request.start_time
        start_dt = datetime.strptime(f"{today} {start_time_str}", "%Y-%m-%d %H:%M")
        stay_minutes = request.stay_minutes or 60
        is_student = request.is_student
        member_shop_ids = request.member_shop_ids or []
        is_member = store.chain_name in member_shop_ids
        
        # 最安プランを検索
        cheapest_plan = find_cheapest_plan_for_store(store, start_dt, stay_minutes, is_member, is_student)
            
        if cheapest_plan is None:
            plans = []
        else:
            # 単一の最安プランから PlanDetail を作成
            option = cheapest_plan["option"]
            pricing_plan = cheapest_plan["plan_name"]
            
            list=[]
            list.append(option.customer_type.value)
            plans = [
                PlanDetail(
                    plan_name=pricing_plan,
                    unit=option.unit_type.value,
                    price=cheapest_plan["total_price"],
                    price_per_30_min=calculate_price_per_30min(option, cheapest_plan["total_price"], stay_minutes),
                    start=option.pricing_plan.start_time if option.pricing_plan else "",
                    end=option.pricing_plan.end_time if option.pricing_plan else "",
                    customer_type=list,
                )
            ]
        
        return GetDetailResponse(
            shop_id=str(store.id), 
            name=store.store_name, 
            plans=plans
        )
            
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shop_id format")
    except Exception as e:
        print(f"Error in get_shop_detail: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

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

# @app.post("/search", response_model=SearchResponse)
# async def search_shops(request: SearchRequest):
#     """
#     検索条件に合致するカラオケ店舗の最安値プランを返すエンドポイント。
#     - 店舗ごとに最安値プランを1件返す
#     - 店舗情報・最安値・プラン名などを含む
#     - 緯度・経度・半径が指定されていれば、その範囲内の店舗のみ対象
#     """
#     results = []
#     today = datetime.now().date()
#     start_time_str = request.start_time
#     start_dt = datetime.strptime(f"{today} {start_time_str}", "%Y-%m-%d %H:%M")
#     stay_minutes = request.stay_minutes or 60
#     is_student = request.is_student
#     member_shop_ids = request.member_shop_ids or []
#     latitude = getattr(request, "latitude", None)
#     longitude = getattr(request, "longitude", None)
#     radius = getattr(request, "radius", None)
#     filtered_stores = dummy_stores
#     if latitude is not None and longitude is not None and radius is not None:
#         from app.utils import haversine

#         filtered_stores = [
#             s for s in dummy_stores if haversine(latitude, longitude, s.latitude, s.longitude) <= radius
#         ]
#     for store in filtered_stores:
#         is_member = store.chain_name in member_shop_ids
#         result = find_cheapest_plan_for_store(store, start_dt, stay_minutes, is_member, is_student)
#         if not result:
#             continue
#         # 距離計算
#         distance = None
#         if latitude is not None and longitude is not None and store.latitude is not None and store.longitude is not None:
#             from app.utils import haversine

#             distance = haversine(latitude, longitude, store.latitude, store.longitude)
#         shop_detail = ShopDetail(
#             shop_id=str(store.id),
#             name=store.store_name,
#             price_per_person=int(result["total_price"]),
#             icon_url=store.chain_name,
#             drink_type=", ".join(result["drink_type"]) if result["drink_type"] else None,  # リストを文字列に変換
#             phone=store.phone_number,
#             all_plans=[result["plan_name"]],
#             latitude=store.latitude,
#             longitude=store.longitude,
#             distance=distance,
#         )
#         results.append(shop_detail)
#     return SearchResponse(results=results)

# # is_store_open関数のテスト用
# @app.get("/store/{store_id}/is_open")
# def check_store_open_status(
#     store_id: int, dt: Annotated[datetime, Query(description="チェックしたい日時（例: 2025-06-20T01:00:00）")] = ...
# ):
#     # 対象店舗を探す
#     store = next((s for s in dummy_stores if s.id == store_id), None)
#     if not store:
#         raise HTTPException(status_code=404, detail="Store not found")

#     is_open = is_store_open(store, dt)

#     return {"store_id": store.id, "store_name": store.store_name, "datetime": dt.isoformat(), "is_open": is_open}


@app.get("/hello")
async def hello():
    """
    ヘルスチェック用エンドポイント。
    """
    return {"message": "Hello!"}
