from sqlmodel import Session

from .db import engine
from .dummy_karaoke_stores import dummy_stores
from .models import (
    BusinessHourDB,
    CustomerType,
    DayType,
    KaraokeStoreDB,
    PlanOptionDB,
    PricingPlanDB,
    TaxType,
    UnitType,
)

# str→Enum変換用
DAY_MAP = {d.value: d for d in DayType}
CUST_MAP = {c.value: c for c in CustomerType}
TAX_MAP = {t.value: t for t in TaxType}
UNIT_MAP = {u.value: u for u in UnitType}


def seed_from_dummy():
    with Session(engine) as session:
        for store in dummy_stores:
            store_db = KaraokeStoreDB(
                id=store.id,
                store_name=store.store_name,
                latitude=store.latitude,
                longitude=store.longitude,
                phone_number=store.phone_number,
                tax_type=TAX_MAP[store.tax_type],
                chain_name=store.chain_name,
            )
            session.add(store_db)
            session.flush()

            # BusinessHour
            for bh in store.business_hours:
                bh_db = BusinessHourDB(
                    day_type=DAY_MAP.get(bh.day_type, DayType.mon),
                    start_time=bh.start_time,
                    end_time=bh.end_time,
                    karaoke_store_id=store_db.id,
                )
                session.add(bh_db)

            # PricingPlan
            for plan in store.pricing_plans:
                plan_db = PricingPlanDB(
                    plan_name=plan.plan_name,
                    start_time=plan.start_time,
                    end_time=plan.end_time,
                    karaoke_store_id=store_db.id,
                )
                session.add(plan_db)
                session.flush()

                # PlanOption
                for opt in plan.options:
                    days_enum = [DAY_MAP.get(d, DayType.mon) for d in opt.days]
                    days_list = [d.value for d in days_enum]
                    opt_db = PlanOptionDB(
                        days=days_list,
                        customer_type=CUST_MAP.get(opt.customer_type, CustomerType.general),
                        amount=opt.amount,
                        unit_type=UNIT_MAP.get(opt.unit_type, UnitType.per_30min),
                        drink_option=getattr(opt, "drink_option", None),
                        notes=getattr(opt, "notes", ""),
                        pricing_plan_id=plan_db.id,
                    )
                    session.add(opt_db)
        session.commit()


if __name__ == "__main__":
    seed_from_dummy()
