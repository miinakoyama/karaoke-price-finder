from typing import List, Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select, Column, Relationship
from sqlalchemy import Column, Text
from sqlalchemy.types import Enum as SQLEnum, JSON
from enum import Enum

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
    holiday = "holiday"  # 追加
    holiday_eve = "holiday_eve"  # 追加

class TaxType(Enum):
    tax_included = "tax_included"
    tax_excluded = "tax_excluded"

class UnitType(Enum):
    per_30min = "per_30min"
    per_hour = "per_hour"
    free_time = "free_time"
    pack = "pack"
    special = "special"

class KaraokeStoreDB(SQLModel, table=True):
    __tablename__ = "karaoke_store"
    id: int = Field(default=None, primary_key=True)
    store_name: str
    latitude: float
    longitude: float
    phone_number: str
    tax_type: TaxType = Field(sa_column=Column(SQLEnum(TaxType)))
    chain_name: str
    business_hours: List["BusinessHourDB"] = Relationship(back_populates="karaoke_store")
    pricing_plans: List["PricingPlanDB"] = Relationship(back_populates="karaoke_store")

class PricingPlanDB(SQLModel, table=True):
    __tablename__ = "pricing_plan"
    id: int = Field(default=None, primary_key=True)
    plan_name: str
    start_time: str
    end_time: str
    karaoke_store_id: Optional[int] = Field(default=None, foreign_key="karaoke_store.id")
    options: List["PlanOptionDB"] = Relationship(back_populates="pricing_plan")
    karaoke_store: Optional["KaraokeStoreDB"] = Relationship(back_populates="pricing_plans")

class PlanOptionDB(SQLModel, table=True):
    __tablename__ = "plan_option"
    id: int = Field(default=None, primary_key=True)
    days: List[str] = Field(sa_column=Column(JSON))  # strリストに修正
    customer_type: CustomerType = Field(sa_column=Column(SQLEnum(CustomerType)))
    amount: int
    unit_type: UnitType = Field(sa_column=Column(SQLEnum(UnitType)))
    drink_option: Optional[str] = ""
    notes: Optional[str] = ""
    pricing_plan_id: Optional[int] = Field(default=None, foreign_key="pricing_plan.id")
    pricing_plan: Optional["PricingPlanDB"] = Relationship(back_populates="options")

class BusinessHourDB(SQLModel, table=True):
    __tablename__ = "business_hour"
    id: int = Field(default=None, primary_key=True)
    day_type: DayType = Field(sa_column=Column(SQLEnum(DayType)))
    start_time: str
    end_time: str
    karaoke_store_id: Optional[int] = Field(default=None, foreign_key="karaoke_store.id")
    karaoke_store: Optional["KaraokeStoreDB"] = Relationship(back_populates="business_hours")
