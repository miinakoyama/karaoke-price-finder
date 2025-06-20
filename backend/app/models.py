from dataclasses import dataclass, field
from typing import List, Literal

CustomerType = Literal["student", "member", "general"]
DayType = Literal["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
TaxType = Literal["tax_included", "tax_excluded"]
UnitType = Literal["per_30min", "per_hour", "free_time", "pack", "special"]


@dataclass
class PlanOption:
    days: List[DayType]
    customer_type: CustomerType
    amount: int
    unit_type: UnitType
    notes: str = ""


@dataclass
class PricingPlan:
    plan_name: str
    start_time: str
    end_time: str
    options: List[PlanOption] = field(default_factory=list)


@dataclass
class BusinessHour:
    day_type: DayType
    start_time: str
    end_time: str


@dataclass
class KaraokeStore:
    id: int
    store_name: str
    latitude: float
    longitude: float
    phone_number: str
    business_hours: List[BusinessHour]
    tax_type: TaxType
    chain_name: str
    pricing_plans: List[PricingPlan] = field(default_factory=list)
    drink_type: List[str]
