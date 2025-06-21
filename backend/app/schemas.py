from pydantic import BaseModel
from typing import List, Optional, Literal

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