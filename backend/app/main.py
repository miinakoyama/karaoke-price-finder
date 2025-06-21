from datetime import datetime
from typing import Annotated, List, Optional, Literal
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends,FastAPI, HTTPException, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from app.dummy_karaoke_stores import dummy_stores
from app.utils import (
    find_cheapest_plan_for_store,
    is_store_open,
    list_available_plans_for_store,
)

from sqlmodel import Field, Session, SQLModel, create_engine, select, Column, Relationship
from sqlalchemy import Column, Text

from enum import Enum
from sqlalchemy.types import Enum as SQLEnum

class CustomerType(Enum):
    student = "student"
    member = "member"
    general = "general"

class DayType(Enum):
    mon = "mon"
    tue = "tue"
    wed = "wed"
    thu = "thu"
    fri = "fri"
    sat = "sat"
    sun = "sun"

class TaxType(Enum):
    tax_included = "tax_included"
    tax_excluded = "tax_excluded"

class UnitType(Enum):
    per_30min = "per_30min"
    per_hour = "per_hour"
    free_time = "free_time"
    pack = "pack"
    special = "special"


class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str


class HeroPublic(HeroBase):
    id: int

class HeroCreate(HeroBase):
    secret_name: str

class PlanOptionDB(SQLModel, table=True):
    __tablename__ = "plan_option"
    id: int = Field(default=None, primary_key=True)  # ← 主キーを追加
    days: DayType = Field(sa_column=Column(SQLEnum(DayType)))
    # days: List[DayType]
    customer_type: CustomerType = Field(sa_column=Column(SQLEnum(CustomerType)))
    amount: int
    unit_type: UnitType = Field(sa_column=Column(SQLEnum(UnitType)))
    notes: str = ""
    # 外部キー：どのプランに属するか
    pricing_plan_id: Optional[int] = Field(default=None, foreign_key="pricing_plan.id")
    # リレーションシップ：親のPricingPlanにアクセス
    pricing_plan: Optional["PricingPlanDB"] = Relationship(back_populates="options")


class PricingPlanDB(SQLModel, table=True):
    __tablename__ = "pricing_plan"
    id: int = Field(default=None, primary_key=True)  # ← 主キーを追加
    plan_name: str
    start_time: str
    end_time: str
    # 外部キー：どの店舗のプランか
    karaoke_store_id: Optional[int] = Field(default=None, foreign_key="karaoke_store.id")
    # リレーションシップ：子のPlanOptionにアクセス
    options: List[PlanOptionDB] = Relationship(back_populates="pricing_plan")
    # リレーションシップ：親のKaraokeStoreにアクセス
    karaoke_store: Optional["KaraokeStoreDB"] = Relationship(back_populates="pricing_plans")

    # options: List[PlanOptionDB] = field(default_factory=list)

class BusinessHourDB(SQLModel, table=True):
    __tablename__ = "business_hour"
    id: int = Field(default=None, primary_key=True)  # ← 主キーを追加
    day_type: DayType = Field(sa_column=Column(SQLEnum(DayType)))
    start_time: str
    end_time: str
    # 外部キー：どの店舗の営業時間か
    karaoke_store_id: Optional[int] = Field(default=None, foreign_key="karaoke_store.id")
    # リレーションシップ：親のKaraokeStoreにアクセス
    karaoke_store: Optional["KaraokeStoreDB"] = Relationship(back_populates="business_hours")


class KaraokeStoreDB(SQLModel, table=True):
    __tablename__ = "karaoke_store"
    id: int = Field(default=None, primary_key=True)  # ← 主キーを追加
    store_name: str
    latitude: float
    longitude: float
    phone_number: str
    # business_hours: List[BusinessHour]
    tax_type: TaxType = Field(sa_column=Column(SQLEnum(TaxType)))
    chain_name: str
    # リレーションシップ：子のBusinessHourにアクセス
    business_hours: List[BusinessHourDB] = Relationship(back_populates="karaoke_store")
    # リレーションシップ：子のPricingPlanにアクセス
    pricing_plans: List[PricingPlanDB] = Relationship(back_populates="karaoke_store")

    # pricing_plans: List[PricingPlan] = field(default_factory=list)
    # drink_type: List[str] = field(default_factory=list)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# テーブルの作成
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# セッションの作成
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React側のURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# --- Request/Response Schemas ---
class SearchRequest(BaseModel):
    """
    検索リクエストのパラメータ。
    - 緯度・経度または地名で検索起点を指定
    - 利用開始時刻、利用時間、人数、学割・会員情報、検索半径など
    """

    latitude: Optional[float] = None
    longitude: Optional[float] = None
    place_name: Optional[str] = None  # 地名での検索も可能に
    stay_minutes: Optional[int] = None  # 分数指定
    start_time: str  # 開始時刻（例: "18:00"）
    group_size: int
    is_student: bool
    member_shop_ids: Optional[List[str]] = None  # 会員情報
    radius: int  # 追加: 検索半径（メートル単位など）


class ShopDetail(BaseModel):
    """
    検索結果・店舗詳細レスポンスの1店舗分の情報。
    - 店舗ID、店舗名、最安値、チェーン名、電話番号、位置情報、最安値プラン名など
    """
    shop_id: str
    name: str
    price_per_person: int
    icon_url: Optional[str]
    drink_type: Optional[str]
    phone: Optional[str]
    all_plans: List[str]
    latitude: Optional[float]
    longitude: Optional[float]
    distance: Optional[float] = None  # 追加: 現在地からの直線距離（メートル）


class SearchResponse(BaseModel):
    """
    検索結果のレスポンス。
    - 店舗ごとの詳細情報リスト
    """

    results: List[ShopDetail]


class PlanDetail(BaseModel):
    """
    プラン詳細情報。
    - 単位種別、金額、30分単価、時間帯、顧客種別
    """

    plan_name: str
    unit: str
    price: int
    price_per_30_min: Optional[int] = None
    start: str
    end: str
    customer_type: List[str]


class GetDetailRequest(BaseModel):
    """
    店舗詳細取得リクエスト。
    - 店舗ID、利用開始時刻、利用時間、学割・会員情報
    """

    shop_id: str
    start_time: str  # "HH:MM" format
    stay_minutes: Optional[int] = 60
    is_student: bool = False
    member_shop_ids: Optional[List[str]] = None


class GetDetailResponse(BaseModel):
    """
    店舗詳細取得レスポンス。
    - 店舗ID、店舗名、該当条件下での全プラン詳細リスト
    """

    shop_id: str
    name: str
    plans: List[PlanDetail]
# PlanDetailTest モデルのpriceはprimary_key=Trueを外す

def seed_plan_option_data():
    with Session(engine) as session:
        # 1. KaraokeStoreDB
        store = session.get(KaraokeStoreDB, 1)
        if not store:
            store = KaraokeStoreDB(
                id=1,
                store_name="カラオケ太郎 渋谷店",
                latitude=35.6595,
                longitude=139.7005,
                phone_number="03-1234-5678",
                tax_type=TaxType.tax_excluded,
                chain_name="カラオケ太郎"
            )
            session.add(store)

        # 2. PricingPlanDB
        plan = session.get(PricingPlanDB, 1)
        if not plan:
            plan = PricingPlanDB(
                id=1,
                plan_name="昼のフリータイム",
                start_time="11:00",
                end_time="18:00",
                karaoke_store_id=store.id
            )
            session.add(plan)

        # 3. PlanOptionDB
        option = session.get(PlanOptionDB, 1)
        if not option:
            option = PlanOptionDB(
                id=1,
                customer_type=CustomerType.member,
                amount=1200,
                unit_type=UnitType.per_hour,
                notes="会員限定プラン",
                days=DayType.sun,
                pricing_plan_id=plan.id
            )
            session.add(option)

        # 4. BusinessHourDB
        bh = session.get(BusinessHourDB, 1)
        if not bh:
            bh = BusinessHourDB(
                id=1,
                day_type=DayType.sun,
                start_time="10:00",
                end_time="23:00",
                karaoke_store_id=store.id
            )
            session.add(bh)

        session.commit()
        print("✅ シードデータを挿入しました")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    seed_plan_option_data()


@app.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

@app.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@app.get("/plan_option/", response_model=list[PlanOptionDB])
def read_plan(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    plans = session.exec(select(PlanOptionDB).offset(offset).limit(limit)).all()
    return plans

@app.get("/pricing_plan/", response_model=list[PricingPlanDB])
def read_plan(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    plans = session.exec(select(PricingPlanDB).offset(offset).limit(limit)).all()
    return plans

@app.get("/business_hour/", response_model=list[BusinessHourDB])
def read_plan(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    plans = session.exec(select(BusinessHourDB).offset(offset).limit(limit)).all()
    return plans


@app.get("/karaoke/", response_model=list[KaraokeStoreDB])
def read_plan(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    test = session.exec(select(KaraokeStoreDB).offset(offset).limit(limit)).all()
    return test


@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero



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
