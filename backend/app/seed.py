from .models import CustomerType,DayType,TaxType,UnitType,PlanOptionDB,PricingPlanDB,BusinessHourDB,KaraokeStoreDB
from sqlmodel import Field, Session, SQLModel, create_engine, select, Column, Relationship
from .db import engine

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
