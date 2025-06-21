from pydantic import BaseModel
from typing import List, Optional, Literal
from pydantic import Field

# --- Request/Response Schemas ---
class SearchRequest(BaseModel):
    latitude: float = Field(..., description="緯度", examples=[35.66287926979908])
    longitude: float = Field(..., description="経度", examples=[139.73315145767197])
    radius: float = Field(..., description="検索範囲(半径m)", examples=[500])
    start_time: str = Field(..., description="開始時刻", examples=["18:00"])
    stay_minutes: int = Field(..., description="利用時間(min.)", examples=[120])
    group_size: int = Field(..., description="人数", examples=[3])
    is_student: bool = Field(..., description="学割利用の有無", examples=[True])
    member_chains: Optional[List[str]] = Field(None, description="会員チェーン名リスト", examples=[["カラオケ太郎", "カラオケ舘"]])

class SearchResultItem(BaseModel):
    store_id: int = Field(..., description="店舗ID", examples=[1])
    chain_name: str = Field(..., description="チェーン名", examples=["カラオケ舘"])
    store_name: str = Field(..., description="店舗名", examples=["六本木本店"])
    lowest_price_per_person: int = Field(..., description="最安値(円/人)", examples=[800])
    drink_option: str = Field(..., description="ドリンク条件", examples=["ドリンク付"])
    distance: float = Field(..., description="直線距離(m)", examples=[200.5])


class SearchResponse(BaseModel):
    results: List[SearchResultItem]


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
    member_chains: Optional[List[str]] = None


class GetDetailResponse(BaseModel):
    """
    店舗詳細取得レスポンス。
    - 店舗ID、店舗名、該当条件下での全プラン詳細リスト
    """

    shop_id: str
    name: str
    plans: List[PlanDetail]
# PlanDetailTest モデルのpriceはprimary_key=Trueを外す
