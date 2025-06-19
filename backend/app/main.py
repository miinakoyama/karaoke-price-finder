from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from utils import stores, find_cheapest_plan,find_plans
from datetime import datetime

app = FastAPI()

# --- Request/Response Schemas ---
class SearchRequest(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    place_name: Optional[str] = None  # 地名での検索も可能に
    stay_minutes: Optional[int] = None  # 分数指定
    is_free_time: Optional[bool] = None  # フリータイム指定
    start_time: str  # 開始時刻（例: "18:00"）
    group_size: int
    is_student: bool
    member_shop_ids: Optional[List[str]] = None #会員情報
    radius: int  # 追加: 検索半径（メートル単位など）

    @classmethod
    def validate_location(cls, values):
        lat, lon, place = values.get('latitude'), values.get('longitude'), values.get('place_name')
        if (lat is not None and lon is not None) or place is not None:
            return values
        raise ValueError('latitude/longitudeまたはplace_nameのいずれかを指定してください')

    class Config:
        schema_extra = {
            "example": {
                "latitude": 35.658034,
                "longitude": 139.701636,
                "place_name": "渋谷駅",
                "stay_minutes": 60,
                "is_free_time": False,
                "start_time": "18:00",
                "group_size": 3,
                "is_student": True,
                "member_shop_ids": ["shop1", "shop2"],
                "radius": 1000
            }
        }

class ShopDetail(BaseModel):
    # リスト画面で使用
    shop_id: str
    name: str
    price_per_person: int
    icon_url: Optional[str]
    drink_type: str
    # walk_minutes: int
    # rating: float

    # 詳細画面で使用
    phone: Optional[str]
    all_plans: List[str]
    latitude: Optional[float]
    longitude: Optional[float]


class SearchResponse(BaseModel):
    results: List[ShopDetail]  # 店舗詳細情報をまとめて返す

class PlanDetail(BaseModel):
    unit: str
    price: int
    price_per_30_min: Optional[int] = None
    start: str
    end: str
    customer_type: List[str]

class GetDetailRequest(BaseModel):
    shop_id: str
    start_time: str  # "HH:MM" format
    stay_minutes: Optional[int] = 60
    is_student: bool = False
    member_shop_ids: Optional[List[str]] = None

class GetDetailResponse(BaseModel):
    shop_id: str
    name: str
    plans: List[PlanDetail]
@app.post("/get_detail", response_model=GetDetailResponse)
async def get_shop_detail(request: GetDetailRequest):
    try:
        # shop_idからstoreを取得
        shop_idx = int(request.shop_id)
        if shop_idx < 0 or shop_idx >= len(stores):
            raise HTTPException(status_code=404, detail="Shop not found")
        
        store = stores[shop_idx]
        
        # 開始時刻をdatetimeに変換
        today = datetime.now().date()
        start_time_str = request.start_time
        start_dt = datetime.strptime(f"{today} {start_time_str}", "%Y-%m-%d %H:%M")
        stay_minutes = request.stay_minutes or 60
        is_student = request.is_student
        
        # メンバーかどうかの判定
        is_member = store.attribute in (request.member_shop_ids or [])
        
        print(f"Getting details for store: {store.name}, is_member: {is_member}")
        
        # find_plansを呼び出してプラン一覧を取得
        plans_data = find_plans(store.rules, start_dt, is_member, is_student, stay_minutes)
        
        # レスポンス用のプランリストを作成
        plans = []
        for plan_data in plans_data:
            plan = PlanDetail(
                unit=plan_data["unit"],
                price=int(plan_data["price"]),
                price_per_30_min=plan_data["price_per_30_min"],
                start=plan_data["start"],
                end=plan_data["end"],
                customer_type=plan_data["customer_type"]
            )
            plans.append(plan)
        
        return GetDetailResponse(
            shop_id=request.shop_id,
            name=store.name,
            plans=plans
        )
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shop_id format")
    except IndexError:
        raise HTTPException(status_code=404, detail="Shop not found")
    except Exception as e:
        print(f"Error in get_shop_detail: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
# --- Endpoints ---
@app.post("/search", response_model=SearchResponse)
async def search_shops(request: SearchRequest):
    # ダミーデータのストア一覧を利用
    results = []
    # 開始時刻をdatetimeに変換（仮で本日日付を利用）
    today = datetime.now().date()
    start_time_str = request.start_time
    start_dt = datetime.strptime(f"{today} {start_time_str}", "%Y-%m-%d %H:%M")
    stay_minutes = request.stay_minutes or 60
    is_student = request.is_student

    for idx, store in enumerate(stores):
        is_member = store.attribute in (request.member_shop_ids or [])
        # print("store.attribute")
        print(store.attribute,"is=member = ",is_member)
        # print(is_member)
        plan_type, price, ok = find_cheapest_plan(store.rules, start_dt, is_member, is_student, stay_minutes)
        if not ok:
            continue
        shop_detail = ShopDetail(
            shop_id=str(idx),
            name=store.name,
            price_per_person=int(price),
            icon_url=None,
            drink_type="ソフトドリンクバー",
            phone=store.phone,
            all_plans=[plan_type],
            latitude=store.lat,
            longitude=store.lon
        )
        results.append(shop_detail)
    return SearchResponse(results=results)

@app.get("/hello")
async def hello():
    """ヘルスチェック"""
    return {"message": "Hello!"}
