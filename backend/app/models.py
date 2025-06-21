from typing import List, Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select, Column, Relationship
from sqlalchemy import Column, Text

from sqlalchemy.types import Enum as SQLEnum

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
