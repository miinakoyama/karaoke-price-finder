from typing import List, Optional

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    latitude: float = Field(..., description="緯度", examples=[35.66287926979908])
    longitude: float = Field(..., description="経度", examples=[139.73315145767197])
    radius: float = Field(..., description="検索範囲(半径m)", examples=[500])
    start_time: str = Field(..., description="開始時刻", examples=["18:00"])
    stay_minutes: int = Field(..., description="利用時間(min.)", examples=[120])
    group_size: int = Field(..., description="人数", examples=[3])
    is_student: bool = Field(..., description="学割利用の有無", examples=[True])
    member_chains: Optional[List[str]] = Field(
        None, description="会員チェーン名リスト", examples=[["カラオケ太郎", "カラオケ舘"]]
    )


class PriceBreakdown(BaseModel):
    plan_name: str = Field(..., description="適用プラン名", examples=["昼フリータイム"])
    time_range: str = Field(..., description="適用時間帯", examples=["11:00~20:00"])
    total_price: int = Field(..., description="合計金額(円)", examples=[1200])


class SearchResultItem(BaseModel):
    store_id: int = Field(..., description="店舗ID", examples=[1])
    chain_name: str = Field(..., description="チェーン名", examples=["カラオケ舘"])
    store_name: str = Field(..., description="店舗名", examples=["六本木本店"])
    lowest_price_per_person: int = Field(..., description="最安値(円/人)", examples=[800])
    drink_option: str = Field(..., description="ドリンク条件", examples=["ドリンク付"])
    distance: float = Field(..., description="直線距離(m)", examples=[200.5])
    latitude: Optional[float] = Field(..., description="緯度", examples=[35.66287926979908])
    longitude: Optional[float] = Field(..., description="経度", examples=[139.73315145767197])
    phone_number: Optional[str] = Field(..., description="電話番号", examples=["03-1234-5678"])
    price_breakdown: Optional[List[PriceBreakdown]] = Field(None, description="最安値の計算根拠リスト")


class SearchResponse(BaseModel):
    results: List[SearchResultItem]


class PlanDetail(BaseModel):
    plan_name: str = Field(..., description="プラン名", examples=["2時間パック"])
    general_price: Optional[int] = Field(..., description="一般料金(円)", examples=[1000])
    student_price: Optional[int] = Field(..., description="学生料金(円)", examples=[800])
    member_price: Optional[int] = Field(..., description="会員料金(円)", examples=[700])
    time_range: Optional[str] = Field(
        None, description="プランの時間帯（例: '11:00~14:00'）", examples=["11:00~14:00"]
    )


class StoreDetailResponse(BaseModel):
    store_id: int = Field(..., description="店舗ID", examples=[1])
    store_name: str = Field(..., description="店舗名", examples=["六本木本店"])
    phone_number: Optional[str] = Field(None, description="電話番号", examples=["03-1234-5678"])
    plans: List[PlanDetail] = Field(..., description="利用可能プラン一覧")
