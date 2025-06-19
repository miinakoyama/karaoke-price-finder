from app.models import BusinessHour, KaraokeStore, PlanOption, PricingPlan

dummy_stores = [
    KaraokeStore(
        id=1,
        store_name="カラオケまねきねこ 六本木店",
        latitude=35.6595,
        longitude=139.7005,
        phone_number="03-1234-5678",
        business_hours=[
            BusinessHour(day_type=day, start_time="00:00", end_time="24:00")
            for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        ],
        tax_type="tax_included",
        chain_name="まねきねこ",
        pricing_plans=[
            PricingPlan(
                plan_name="昼フリータイム",
                start_time="11:00",
                end_time="20:00",
                options=[
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="general",
                        amount=1500,
                        unit_type="free_time",
                    ),
                    PlanOption(days=["sat", "sun"], customer_type="student", amount=1200, unit_type="free_time"),
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="student",
                        amount=1300,
                        unit_type="free_time",
                    ),  # 平日学生用を追加
                ],
            ),
            PricingPlan(
                plan_name="30分料金",
                start_time="07:00",
                end_time="18:00",
                options=[
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="general",
                        amount=319,
                        unit_type="per_30min",
                    ),
                    PlanOption(days=["sat", "sun"], customer_type="member", amount=273, unit_type="per_30min"),
                ],
            ),
        ],
    ),
    KaraokeStore(
        id=2,
        store_name="ビッグエコー赤坂駅前店",
        latitude=35.6745,
        longitude=139.7366,
        phone_number="03-2345-6789",
        business_hours=[
            BusinessHour(day_type="mon", start_time="14:00", end_time="05:00"),
            BusinessHour(day_type="sat", start_time="14:00", end_time="05:00"),
            BusinessHour(day_type="fri", start_time="14:00", end_time="05:00"),  # holiday_eve→fri
        ],
        tax_type="tax_excluded",
        chain_name="ビッグエコー",
        pricing_plans=[
            PricingPlan(
                plan_name="夜パック",
                start_time="18:00",
                end_time="23:00",
                options=[
                    PlanOption(days=["fri", "sat"], customer_type="general", amount=2000, unit_type="pack"),
                    PlanOption(days=["fri", "sat"], customer_type="student", amount=1500, unit_type="pack"),
                ],
            ),
            PricingPlan(
                plan_name="30分料金",
                start_time="14:00",
                end_time="18:00",
                options=[
                    PlanOption(
                        days=["mon", "tue", "wed", "thu"], customer_type="general", amount=360, unit_type="per_30min"
                    ),
                    PlanOption(
                        days=["mon", "tue", "wed", "thu"], customer_type="student", amount=180, unit_type="per_30min"
                    ),
                ],
            ),
            PricingPlan(
                plan_name="スペシャル学割パック",
                start_time="09:00",
                end_time="17:00",
                options=[
                    # holiday_eve→fri
                    PlanOption(
                        days=["fri"],
                        customer_type="student",
                        amount=0,
                        unit_type="special",
                        notes="学生証提示必須・中高生限定",
                    )
                ],
            ),
        ],
    ),
    KaraokeStore(
        id=3,
        store_name="カラオケパセラ六本木店",
        latitude=35.6618,
        longitude=139.7353,
        phone_number="03-3456-7890",
        business_hours=[
            BusinessHour(day_type="fri", start_time="17:00", end_time="07:00"),
            BusinessHour(day_type="sat", start_time="11:00", end_time="07:00"),
            # holiday_eve→fri
        ],
        tax_type="tax_included",
        chain_name="パセラ",
        pricing_plans=[
            PricingPlan(
                plan_name="オールナイトフリータイム",
                start_time="22:00",
                end_time="05:00",
                options=[
                    PlanOption(days=["fri", "sat"], customer_type="general", amount=4000, unit_type="free_time"),
                    PlanOption(days=["fri", "sat"], customer_type="member", amount=3500, unit_type="free_time"),
                ],
            ),
            PricingPlan(
                plan_name="1時間パック",
                start_time="11:00",
                end_time="17:00",
                options=[
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="general",
                        amount=1000,
                        unit_type="per_hour",
                    ),
                ],
            ),
        ],
    ),
]
