from datetime import datetime

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
    create_db_and_tables,
)
from .models import (
    KaraokeStoreDB,
    PlanOptionDB,
)
from .schemas import GetDetailRequest, GetDetailResponse, PlanDetail, SearchRequest, SearchResponse, SearchResultItem
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

            list = []
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

        return GetDetailResponse(shop_id=str(store.id), name=store.store_name, plans=plans)

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shop_id format")
    except Exception as e:
        print(f"Error in get_shop_detail: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/stores/{store_id}", response_model=GetDetailResponse)
async def get_store_detail(
    store_id: int,
    session: SessionDep,
    start_time: str = Query(..., description="利用開始時刻（例: '18:00'）"),
    stay_minutes: int = Query(60, description="利用時間（分）"),
    is_student: bool = Query(False, description="学生区分"),
    member_shop_ids: List[str] = Query([], description="会員店舗IDのリスト")
):
    """
    指定した店舗ID・利用開始時刻・利用時間・会員/学生区分で、
    条件に合致する全プラン詳細を返すエンドポイント。
    """
    try:
        shop_id = store_id

        # Dependency Injectionで受け取ったセッションを使用
        store = session.get(KaraokeStoreDB, shop_id)
        if store is None:
            raise HTTPException(status_code=404, detail="Shop not found")

        today = datetime.now().date()
        start_time_str = start_time
        start_dt = datetime.strptime(f"{today} {start_time_str}", "%Y-%m-%d %H:%M")
        is_member = store.chain_name in member_shop_ids

        # 最安プランを検索
        cheapest_plan = find_cheapest_plan_for_store(store, start_dt, stay_minutes, is_member, is_student)

        if cheapest_plan is None:
            plans = []
        else:
            # 単一の最安プランから PlanDetail を作成
            option = cheapest_plan["option"]
            pricing_plan = cheapest_plan["plan_name"]

            list = []
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

        return GetDetailResponse(shop_id=str(store.id), name=store.store_name, plans=plans)

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shop_id format")
    except Exception as e:
        print(f"Error in get_store_detail: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
# TODO: store_detail更新
# @app.get("/stores/{store_id}", response_model=StoreDetailResponse)
# async def get_store_detail(
#     store_id: int,
#     session: SessionDep,
#     start_time: str = Query(..., description="利用開始時刻（例: '18:00'）"),
# ):
#     """
#     指定した店舗ID・利用開始時刻から閉店までの全プラン詳細を返すエンドポイント。
#     """
#     store = session.get(KaraokeStoreDB, store_id)
#     if store is None:
#         raise HTTPException(status_code=404, detail="Shop not found")

#     today = datetime.now().date()
#     start_dt = datetime.strptime(f"{today} {start_time}", "%Y-%m-%d %H:%M")
#     day = start_dt.strftime("%a").lower()

#     # 閉店時刻を取得（当日のbusiness_hoursから）
#     closing_time = None
#     for bh in store.business_hours:
#         if bh.day_type.value == day:
#             closing_time = bh.end_time
#             break
#     if not closing_time:
#         closing_time = "23:59"  # fallback

#     # プランの開始時刻がstart_time以降、かつ終了時刻が閉店時刻以下のものを返す
#     plans = []
#     for plan in store.pricing_plans:
#         # プランの時間帯が条件に合うか
#         if plan.start_time >= start_time and plan.end_time <= closing_time:
#             for option in plan.options:
#                 plan_detail = PlanDetail(
#                     plan_name=plan.plan_name,
#                     general_price=option.amount if option.customer_type.value == "general" else None,
#                     student_price=option.amount if option.customer_type.value == "student" else None,
#                     member_price=option.amount if option.customer_type.value == "member" else None,
#                 )
#                 plans.append(plan_detail)

#     return StoreDetailResponse(store_id=store.id, store_name=store.store_name, plans=plans)


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
        # 会員判定
        is_member = is_member_store(store, getattr(request, 'member_chains', None))
        result = find_cheapest_plan_for_store(store, start_dt, request.stay_minutes, is_member, request.is_student)
        if not result:
            continue
        results.append(
            SearchResultItem(
                store_id=store.id,
                chain_name=store.chain_name,
                store_name=store.store_name,
                lowest_price_per_person=int(result["total_price"]),
                drink_option=result.get("drink_option", ""),
                distance=distance,
            )
        )
    return SearchResponse(results=results)


@app.get("/hello")
async def hello():
    """
    ヘルスチェック用エンドポイント。
    """
    return {"message": "Hello!"}
