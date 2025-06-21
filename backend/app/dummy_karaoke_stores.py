from app.models import BusinessHour, KaraokeStore, PlanOption, PricingPlan

dummy_stores = [
    KaraokeStore(
        id=1,
        store_name="カラオケまねきねこ 六本木店",
        latitude=35.6595,
        longitude=139.7005,
        phone_number="03-1234-5678",
        business_hours=[
            BusinessHour(day_type=day, start_time="00:00", end_time="00:00")
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
                        drink_option="ドリンクバー付き"
                    ),
                    PlanOption(
                        days=["sat", "sun"], 
                        customer_type="student", 
                        amount=1200, 
                        unit_type="free_time",
                        drink_option="ドリンクバー付き"
                    ),
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="student",
                        amount=1300,
                        unit_type="free_time",
                        drink_option="ドリンクバー付き"
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
                        drink_option="ワンドリンク制"
                    ),
                    PlanOption(
                        days=["sat", "sun"],
                        customer_type="member",
                        amount=273,
                        unit_type="per_30min",
                        drink_option="ワンドリンク制"
                    ),
                ],
            ),
        ],
        drink_type=["ソフトドリンクバー", "ワンドリンク制"]
    ),
    KaraokeStore(
        id=2,
        store_name="ビッグエコー 赤坂駅前店",
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
                    PlanOption(
                        days=["fri", "sat"],
                        customer_type="general",
                        amount=2000,
                        unit_type="pack",
                        drink_option="1ドリンクオーダー制"
                    ),
                    PlanOption(
                        days=["fri", "sat"],
                        customer_type="student",
                        amount=1500,
                        unit_type="pack",
                        drink_option="1ドリンクオーダー制"
                    ),
                ],
            ),
            PricingPlan(
                plan_name="30分料金",
                start_time="14:00",
                end_time="18:00",
                options=[
                    PlanOption(
                        days=["mon", "tue", "wed", "thu"],
                        customer_type="general",
                        amount=360,
                        unit_type="per_30min",
                        drink_option="1ドリンクオーダー制"
                    ),
                    PlanOption(
                        days=["mon", "tue", "wed", "thu"],
                        customer_type="student",
                        amount=180,
                        unit_type="per_30min",
                        drink_option="1ドリンクオーダー制"
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
                        drink_option="1ドリンクオーダー制"
                    )
                ],
            ),
        ],
        drink_type=["1ドリンクオーダー制"]
    ),
    KaraokeStore(
        id=3,
        store_name="カラオケパセラ 六本木店",
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
                    PlanOption(
                        days=["fri", "sat"],
                        customer_type="general",
                        amount=4000,
                        unit_type="free_time",
                        drink_option="1ドリンク付き（アルコール含む）"
                    ),
                    PlanOption(
                        days=["fri", "sat"],
                        customer_type="member",
                        amount=3500,
                        unit_type="free_time",
                        drink_option="1ドリンク付き（アルコール含む）"
                    ),
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
                        drink_option="1ドリンク付き（アルコール含む）"
                    ),
                ],
            ),
        ],
        drink_type=["1ドリンク付き（アルコール含む）"]
    ),
    KaraokeStore(
        id=4,
        store_name="カラオケ館 六本木店",
        latitude=35.663657,
        longitude=139.732032,
        phone_number="03-5410-2244",
        business_hours=[
            # 日～木・祝 12:00～翌5:00
            BusinessHour(day_type=day, start_time="12:00", end_time="05:00")
            for day in ["sun", "mon", "tue", "wed", "thu", "holiday"]
        ] + [
            # 金・土・祝前日 12:00～翌6:00
            BusinessHour(day_type=day, start_time="12:00", end_time="06:00")
            for day in ["fri", "sat", "holiday_eve"]
        ],
        tax_type="tax_included",
        chain_name="カラオケ館",
        pricing_plans=[
            # 30分料金（昼12:00～18:00）
            PricingPlan(
                plan_name="30分料金",
                start_time="12:00",
                end_time="18:00",
                options=[
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="student",
                        amount=240,
                        unit_type="per_30min",
                        drink_option="ソフトドリンク飲み放題"
                    ),
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="member",
                        amount=240,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="general",
                        amount=320,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="student",
                        amount=300,
                        unit_type="per_30min",
                        drink_option="ソフトドリンク飲み放題"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="member",
                        amount=300,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="general",
                        amount=400,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                ],
            ),
            # 30分料金（夜18:00～翌5:00）
            PricingPlan(
                plan_name="30分料金",
                start_time="18:00",
                end_time="05:00",
                options=[
                    PlanOption(
                        days=["sun", "mon", "tue", "wed", "thu", "holiday"],
                        customer_type="member",
                        amount=540,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sun", "mon", "tue", "wed", "thu", "holiday"],
                        customer_type="general",
                        amount=720,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["fri", "sat", "holiday_eve"],
                        customer_type="member",
                        amount=720,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["fri", "sat", "holiday_eve"],
                        customer_type="general",
                        amount=960,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                ],
            ),
            # フリータイム（昼12:00～19:00）
            PricingPlan(
                plan_name="フリータイム",
                start_time="12:00",
                end_time="19:00",
                options=[
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="student",
                        amount=1200,
                        unit_type="free_time",
                        drink_option="ソフトドリンク飲み放題"
                    ),
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="member",
                        amount=1200,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="general",
                        amount=1600,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="student",
                        amount=1500,
                        unit_type="free_time",
                        drink_option="ソフトドリンク飲み放題"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="member",
                        amount=1500,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="general",
                        amount=2000,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                ],
            ),
            # フリータイム（深夜23:00～翌5:00／学生は18:00～）
            PricingPlan(
                plan_name="フリータイム",
                start_time="23:00",
                end_time="05:00",
                options=[
                    PlanOption(
                        days=["sun", "mon", "tue", "wed", "thu", "holiday"],
                        customer_type="student",
                        amount=770,
                        unit_type="free_time",
                        drink_option="ソフトドリンク飲み放題（学生18:00～）"
                    ),
                    PlanOption(
                        days=["sun", "mon", "tue", "wed", "thu", "holiday"],
                        customer_type="member",
                        amount=2700,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sun", "mon", "tue", "wed", "thu", "holiday"],
                        customer_type="general",
                        amount=3600,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["fri", "sat", "holiday_eve"],
                        customer_type="student",
                        amount=1650,
                        unit_type="free_time",
                        drink_option="ソフトドリンク飲み放題"
                    ),
                    PlanOption(
                        days=["fri", "sat", "holiday_eve"],
                        customer_type="member",
                        amount=3600,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["fri", "sat", "holiday_eve"],
                        customer_type="general",
                        amount=4800,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                ],
            ),
        ],
        drink_type=["ソフトドリンク飲み放題", "1ドリンク制"]
    ),
    KaraokeStore(
        id=5,
        store_name="カラオケ館 六本木本店",
        latitude=35.662629,
        longitude=139.733111,
        phone_number="03-5786-9400",
        business_hours=[
            BusinessHour(day_type=day, start_time="12:00", end_time="06:00")
            for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun", "holiday", "holiday_eve"]
        ],
        tax_type="tax_included",
        chain_name="カラオケ館",
        pricing_plans=[
            # 30分料金（昼12:00〜18:00）
            PricingPlan(
                plan_name="30分料金",
                start_time="12:00",
                end_time="18:00",
                options=[
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="student",
                        amount=240,
                        unit_type="per_30min",
                        drink_option="ソフトドリンク飲み放題"
                    ),
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="member",
                        amount=240,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="general",
                        amount=320,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="student",
                        amount=300,
                        unit_type="per_30min",
                        drink_option="ソフトドリンク飲み放題"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="member",
                        amount=300,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="general",
                        amount=400,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                ],
            ),
            # 30分料金（夜18:00〜翌6:00）
            PricingPlan(
                plan_name="30分料金",
                start_time="18:00",
                end_time="06:00",
                options=[
                    PlanOption(
                        days=["sun", "mon", "tue", "wed", "thu", "holiday"],
                        customer_type="member",
                        amount=540,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sun", "mon", "tue", "wed", "thu", "holiday"],
                        customer_type="general",
                        amount=720,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["fri", "sat", "holiday_eve"],
                        customer_type="member",
                        amount=720,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["fri", "sat", "holiday_eve"],
                        customer_type="general",
                        amount=960,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                ],
            ),
            # フリータイム（昼12:00〜19:00）
            PricingPlan(
                plan_name="フリータイム",
                start_time="12:00",
                end_time="19:00",
                options=[
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="student",
                        amount=1200,
                        unit_type="free_time",
                        drink_option="ソフトドリンク飲み放題"
                    ),
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="member",
                        amount=1200,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="general",
                        amount=1600,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="student",
                        amount=1500,
                        unit_type="free_time",
                        drink_option="ソフトドリンク飲み放題"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="member",
                        amount=1500,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="general",
                        amount=2000,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                ],
            ),
            # フリータイム（深夜23:00〜翌5:00／学生は18:00〜）
            PricingPlan(
                plan_name="フリータイム",
                start_time="23:00",
                end_time="05:00",
                options=[
                    PlanOption(
                        days=["sun", "mon", "tue", "wed", "thu", "holiday"],
                        customer_type="student",
                        amount=770,
                        unit_type="free_time",
                        drink_option="ソフトドリンク飲み放題（学生18:00〜）"
                    ),
                    PlanOption(
                        days=["sun", "mon", "tue", "wed", "thu", "holiday"],
                        customer_type="member",
                        amount=2700,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sun", "mon", "tue", "wed", "thu", "holiday"],
                        customer_type="general",
                        amount=3600,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["fri", "sat", "holiday_eve"],
                        customer_type="student",
                        amount=1650,
                        unit_type="free_time",
                        drink_option="ソフトドリンク飲み放題"
                    ),
                    PlanOption(
                        days=["fri", "sat", "holiday_eve"],
                        customer_type="member",
                        amount=3600,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["fri", "sat", "holiday_eve"],
                        customer_type="general",
                        amount=4800,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                ],
            ),
        ],
        drink_type=["ソフトドリンク飲み放題", "1ドリンク制"]
    ),
    KaraokeStore(
        id=6,
        store_name="カラオケ館 赤坂サカス前店",
        latitude=35.671181,
        longitude=139.735894,
        phone_number="03-5573-4861",
        business_hours=[
            # 土〜木・祝 11:30〜翌5:00
            BusinessHour(day_type=day, start_time="11:30", end_time="05:00")
            for day in ["sat", "sun", "mon", "tue", "wed", "thu", "holiday"]
        ] + [
            # 金・祝前日 11:30〜翌6:00
            BusinessHour(day_type=day, start_time="11:30", end_time="06:00")
            for day in ["fri", "holiday_eve"]
        ],
        tax_type="tax_included",
        chain_name="カラオケ館",
        pricing_plans=[
            # 30分料金（11:30〜18:00）
            PricingPlan(
                plan_name="30分料金",
                start_time="11:30",
                end_time="18:00",
                options=[
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="student",
                        amount=140,
                        unit_type="per_30min",
                        drink_option="1ドリンク制 or ドリンクバー＋¥550"
                    ),
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="member",
                        amount=200,
                        unit_type="per_30min",
                        drink_option="1ドリンク制 or ドリンクバー＋¥550"
                    ),
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="general",
                        amount=266,
                        unit_type="per_30min",
                        drink_option="1ドリンク制 or ドリンクバー＋¥550"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="student",
                        amount=200,
                        unit_type="per_30min",
                        drink_option="1ドリンク制 or ドリンクバー＋¥550"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="member",
                        amount=300,
                        unit_type="per_30min",
                        drink_option="1ドリンク制 or ドリンクバー＋¥550"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="general",
                        amount=400,
                        unit_type="per_30min",
                        drink_option="1ドリンク制 or ドリンクバー＋¥550"
                    ),
                ],
            ),
            # 30分料金（18:00〜翌5:00／金・祝前日〜6:00）
            PricingPlan(
                plan_name="30分料金",
                start_time="18:00",
                end_time="05:00",
                options=[
                    PlanOption(
                        days=["sun", "mon", "tue", "wed", "thu", "holiday"],
                        customer_type="member",
                        amount=600,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sun", "mon", "tue", "wed", "thu", "holiday"],
                        customer_type="general",
                        amount=800,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["fri", "sat", "holiday_eve"],
                        customer_type="member",
                        amount=690,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["fri", "sat", "holiday_eve"],
                        customer_type="general",
                        amount=920,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                ],
            ),
            # フリータイム（12:00〜20:00）
            PricingPlan(
                plan_name="フリータイム",
                start_time="12:00",
                end_time="20:00",
                options=[
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="student",
                        amount=700,
                        unit_type="free_time",
                        drink_option="1ドリンク制 or ドリンクバー＋¥550"
                    ),
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="member",
                        amount=1000,
                        unit_type="free_time",
                        drink_option="1ドリンク制 or ドリンクバー＋¥550"
                    ),
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="general",
                        amount=1333,
                        unit_type="free_time",
                        drink_option="1ドリンク制 or ドリンクバー＋¥550"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="student",
                        amount=1000,
                        unit_type="free_time",
                        drink_option="1ドリンク制 or ドリンクバー＋¥550"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="member",
                        amount=1500,
                        unit_type="free_time",
                        drink_option="1ドリンク制 or ドリンクバー＋¥550"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="general",
                        amount=2000,
                        unit_type="free_time",
                        drink_option="1ドリンク制 or ドリンクバー＋¥550"
                    ),
                ],
            ),
            # フリータイム（23:00〜翌5:00／学生18:00〜）
            PricingPlan(
                plan_name="フリータイム",
                start_time="23:00",
                end_time="05:00",
                options=[
                    PlanOption(
                        days=["sun", "mon", "tue", "wed", "thu", "holiday"],
                        customer_type="student",
                        amount=770,
                        unit_type="free_time",
                        drink_option="ドリンクバー付（学生18:00〜）"
                    ),
                    PlanOption(
                        days=["sun", "mon", "tue", "wed", "thu", "holiday"],
                        customer_type="member",
                        amount=3000,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sun", "mon", "tue", "wed", "thu", "holiday"],
                        customer_type="general",
                        amount=4000,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["fri", "sat", "holiday_eve"],
                        customer_type="student",
                        amount=1650,
                        unit_type="free_time",
                        drink_option="ドリンクバー付"
                    ),
                    PlanOption(
                        days=["fri", "sat", "holiday_eve"],
                        customer_type="member",
                        amount=3450,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["fri", "sat", "holiday_eve"],
                        customer_type="general",
                        amount=4600,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                ],
            ),
        ],
        drink_type=["1ドリンク制", "ドリンクバー＋¥550"]
    ),
    KaraokeStore(
        id=7,
        store_name="カラオケ館 赤坂店",
        latitude=35.676384,
        longitude=139.737185,
        phone_number="03-5563-2702",
        business_hours=[
            # 土〜木・祝 11:30〜翌5:00
            BusinessHour(day_type=day, start_time="11:30", end_time="05:00")
            for day in ["sat", "sun", "mon", "tue", "wed", "thu", "holiday"]
        ] + [
            # 金・祝前日 11:30〜翌6:00
            BusinessHour(day_type=day, start_time="11:30", end_time="06:00")
            for day in ["fri", "holiday_eve"]
        ],
        tax_type="tax_included",
        chain_name="カラオケ館",
        pricing_plans=[
            # 30分料金（12:00〜18:00）
            PricingPlan(
                plan_name="30分料金",
                start_time="12:00",
                end_time="18:00",
                options=[
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="student",
                        amount=140,
                        unit_type="per_30min",
                        drink_option="1ドリンク制 or ドリンクバー＋¥550"
                    ),
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="member",
                        amount=200,
                        unit_type="per_30min",
                        drink_option="1ドリンク制 or ドリンクバー＋¥550"
                    ),
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="general",
                        amount=266,
                        unit_type="per_30min",
                        drink_option="1ドリンク制 or ドリンクバー＋¥550"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="student",
                        amount=200,
                        unit_type="per_30min",
                        drink_option="1ドリンク制 or ドリンクバー＋¥550"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="member",
                        amount=300,
                        unit_type="per_30min",
                        drink_option="1ドリンク制 or ドリンクバー＋¥550"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="general",
                        amount=400,
                        unit_type="per_30min",
                        drink_option="1ドリンク制 or ドリンクバー＋¥550"
                    ),
                ],
            ),
            # 30分料金（18:00〜翌5:00／金・祝前日〜6:00）
            PricingPlan(
                plan_name="30分料金",
                start_time="18:00",
                end_time="05:00",
                options=[
                    PlanOption(
                        days=["sun", "mon", "tue", "wed", "thu", "holiday"],
                        customer_type="member",
                        amount=600,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sun", "mon", "tue", "wed", "thu", "holiday"],
                        customer_type="general",
                        amount=800,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["fri", "sat", "holiday_eve"],
                        customer_type="member",
                        amount=690,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["fri", "sat", "holiday_eve"],
                        customer_type="general",
                        amount=920,
                        unit_type="per_30min",
                        drink_option="1ドリンク制"
                    ),
                ],
            ),
            # フリータイム（12:00〜20:00）
            PricingPlan(
                plan_name="フリータイム",
                start_time="12:00",
                end_time="20:00",
                options=[
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="student",
                        amount=700,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="member",
                        amount=1000,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["mon", "tue", "wed", "thu", "fri"],
                        customer_type="general",
                        amount=1333,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="student",
                        amount=1000,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="member",
                        amount=1500,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sat", "sun", "holiday"],
                        customer_type="general",
                        amount=2000,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                ],
            ),
            # フリータイム（23:00〜翌5:00／学生は18:00〜）
            PricingPlan(
                plan_name="フリータイム",
                start_time="23:00",
                end_time="05:00",
                options=[
                    PlanOption(
                        days=["sun", "mon", "tue", "wed", "thu", "holiday"],
                        customer_type="student",
                        amount=770,
                        unit_type="free_time",
                        drink_option="ソフトドリンク飲み放題"
                    ),
                    PlanOption(
                        days=["sun", "mon", "tue", "wed", "thu", "holiday"],
                        customer_type="member",
                        amount=3000,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sun", "mon", "tue", "wed", "thu", "holiday"],
                        customer_type="general",
                        amount=4000,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["fri", "sat", "holiday_eve"],
                        customer_type="student",
                        amount=1650,
                        unit_type="free_time",
                        drink_option="ソフトドリンク飲み放題"
                    ),
                    PlanOption(
                        days=["fri", "sat", "holiday_eve"],
                        customer_type="member",
                        amount=3450,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["fri", "sat", "holiday_eve"],
                        customer_type="general",
                        amount=4600,
                        unit_type="free_time",
                        drink_option="1ドリンク制"
                    ),
                ],
            ),
        ],
        drink_type=["1ドリンク制", "ドリンクバー＋¥550"]
    ),
    KaraokeStore(
        id=8,
        store_name="カラオケ館 赤坂見附店",
        latitude=35.676323,
        longitude=139.736245,
        phone_number="03-3560-7277",
        business_hours=[
            # 土～木・祝 11:30～翌5:00
            BusinessHour(day_type=day, start_time="11:30", end_time="05:00")
            for day in ["sat", "sun", "mon", "tue", "wed", "thu", "holiday"]
        ] + [
            # 金・祝前日 11:30～翌6:00
            BusinessHour(day_type=day, start_time="11:30", end_time="06:00")
            for day in ["fri", "holiday_eve"]
        ],
        tax_type="tax_included",
        chain_name="カラオケ館",
        pricing_plans=[
            # 30分料金（12:00～18:00）
            PricingPlan(
                plan_name="30分料金",
                start_time="12:00",
                end_time="18:00",
                options=[
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="student", amount=140, unit_type="per_30min", drink_option="1ドリンク制 or ドリンクバー＋¥550"),
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="member",  amount=200, unit_type="per_30min", drink_option="1ドリンク制 or ドリンクバー＋¥550"),
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="general", amount=266, unit_type="per_30min", drink_option="1ドリンク制 or ドリンクバー＋¥550"),
                    PlanOption(days=["sat","sun","holiday"],         customer_type="student", amount=200, unit_type="per_30min", drink_option="1ドリンク制 or ドリンクバー＋¥550"),
                    PlanOption(days=["sat","sun","holiday"],         customer_type="member",  amount=300, unit_type="per_30min", drink_option="1ドリンク制 or ドリンクバー＋¥550"),
                    PlanOption(days=["sat","sun","holiday"],         customer_type="general", amount=400, unit_type="per_30min", drink_option="1ドリンク制 or ドリンクバー＋¥550"),
                ],
            ),
            # 30分料金（18:00～翌5:00／金・祝前日～6:00）
            PricingPlan(
                plan_name="30分料金",
                start_time="18:00",
                end_time="05:00",
                options=[
                    PlanOption(days=["sun","mon","tue","wed","thu","holiday"], customer_type="member",  amount=600,  unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["sun","mon","tue","wed","thu","holiday"], customer_type="general", amount=800,  unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["fri","sat","holiday_eve"],          customer_type="member",  amount=690,  unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["fri","sat","holiday_eve"],          customer_type="general", amount=920,  unit_type="per_30min", drink_option="1ドリンク制"),
                ],
            ),
            # フリータイム（12:00～20:00）
            PricingPlan(
                plan_name="フリータイム",
                start_time="12:00",
                end_time="20:00",
                options=[
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="student", amount=700,  unit_type="free_time", drink_option="1ドリンク制 or ドリンクバー＋¥550"),
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="member",  amount=1000, unit_type="free_time", drink_option="1ドリンク制 or ドリンクバー＋¥550"),
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="general", amount=1333, unit_type="free_time", drink_option="1ドリンク制 or ドリンクバー＋¥550"),
                    PlanOption(days=["sat","sun","holiday"],         customer_type="student", amount=1000, unit_type="free_time", drink_option="1ドリンク制 or ドリンクバー＋¥550"),
                    PlanOption(days=["sat","sun","holiday"],         customer_type="member",  amount=1500, unit_type="free_time", drink_option="1ドリンク制 or ドリンクバー＋¥550"),
                    PlanOption(days=["sat","sun","holiday"],         customer_type="general", amount=2000, unit_type="free_time", drink_option="1ドリンク制 or ドリンクバー＋¥550"),
                ],
            ),
            # フリータイム（23:00～翌5:00／学生18:00～）
            PricingPlan(
                plan_name="フリータイム",
                start_time="23:00",
                end_time="05:00",
                options=[
                    PlanOption(days=["sun","mon","tue","wed","thu","holiday"], customer_type="student", amount=770,  unit_type="free_time", drink_option="ソフトドリンク飲み放題"),
                    PlanOption(days=["sun","mon","tue","wed","thu","holiday"], customer_type="member",  amount=3000, unit_type="free_time", drink_option="1ドリンク制"),
                    PlanOption(days=["sun","mon","tue","wed","thu","holiday"], customer_type="general", amount=4000, unit_type="free_time", drink_option="1ドリンク制"),
                    PlanOption(days=["fri","sat","holiday_eve"],          customer_type="student", amount=1650, unit_type="free_time", drink_option="ソフトドリンク飲み放題"),
                    PlanOption(days=["fri","sat","holiday_eve"],          customer_type="member",  amount=3450, unit_type="free_time", drink_option="1ドリンク制"),
                    PlanOption(days=["fri","sat","holiday_eve"],          customer_type="general", amount=4600, unit_type="free_time", drink_option="1ドリンク制"),
                ],
            ),
        ],
        drink_type=["1ドリンク制", "ドリンクバー＋¥550"]
    ),
    KaraokeStore(
        id=9,
        store_name="カラオケまねきねこ 赤坂店",
        latitude=35.674446,
        longitude=139.736134,
        phone_number="03-6441-3200",
        business_hours=[
            BusinessHour(day_type=day, start_time="00:00", end_time="00:00")
            for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun", "holiday", "holiday_eve"]
        ],
        tax_type="tax_included",
        chain_name="まねきねこ",
        pricing_plans=[
            # 朝うた（9:00～12:00／最終受付10:59）
            PricingPlan(
                plan_name="朝うた",
                start_time="09:00",
                end_time="12:00",
                options=[
                    PlanOption(
                        days=["mon","tue","wed","thu","fri","sat","sun","holiday","holiday_eve"],
                        customer_type="member",
                        amount=50,
                        unit_type="special",
                        notes="最終受付10:59／税込55円",
                        drink_option="1ドリンク制"
                    ),
                ],
            ),
            # 昼30分（11:00～18:00）
            PricingPlan(
                plan_name="30分",
                start_time="11:00",
                end_time="18:00",
                options=[
                    PlanOption(
                        days=["mon","tue","wed","thu","fri"],
                        customer_type="member",
                        amount=150,
                        unit_type="per_30min",
                        notes="税込165円",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sat","sun","holiday"],
                        customer_type="member",
                        amount=200,
                        unit_type="per_30min",
                        notes="税込220円",
                        drink_option="1ドリンク制"
                    ),
                ],
            ),
            # フリータイム（11:00～20:00／最終受付17:00平日・18:00週末）
            PricingPlan(
                plan_name="フリータイム",
                start_time="11:00",
                end_time="20:00",
                options=[
                    PlanOption(
                        days=["mon","tue","wed","thu","fri"],
                        customer_type="member",
                        amount=900,
                        unit_type="free_time",
                        notes="最終受付17:00／税込990円",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sat","sun","holiday"],
                        customer_type="member",
                        amount=1_400,
                        unit_type="free_time",
                        notes="最終受付18:00／税込1 540円",
                        drink_option="1ドリンク制"
                    ),
                ],
            ),
            # 昼まふ（11:00～18:00／最終受付16:00・学生限定）
            PricingPlan(
                plan_name="昼まふ",
                start_time="11:00",
                end_time="18:00",
                options=[
                    PlanOption(
                        days=["mon","tue","wed","thu","fri"],
                        customer_type="member",
                        amount=700,
                        unit_type="special",
                        notes="最終受付16:00／短大・大学生・専門学生対象／税込770円",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sat","sun","holiday"],
                        customer_type="member",
                        amount=1_500,
                        unit_type="special",
                        notes="最終受付16:00／短大・大学生・専門学生対象／税込1 650円",
                        drink_option="1ドリンク制"
                    ),
                ],
            ),
            # 夜30分（18:00～翌9:00）
            PricingPlan(
                plan_name="30分",
                start_time="18:00",
                end_time="09:00",
                options=[
                    PlanOption(
                        days=["mon","tue","wed","thu","fri"],
                        customer_type="member",
                        amount=500,
                        unit_type="per_30min",
                        notes="税込550円",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sat","sun","holiday"],
                        customer_type="member",
                        amount=600,
                        unit_type="per_30min",
                        notes="税込660円",
                        drink_option="1ドリンク制"
                    ),
                ],
            ),
            # 夜フリータイム（18:00～5:00／最終受付翌2:00）
            PricingPlan(
                plan_name="フリータイム",
                start_time="18:00",
                end_time="05:00",
                options=[
                    PlanOption(
                        days=["mon","tue","wed","thu","fri"],
                        customer_type="member",
                        amount=2_700,
                        unit_type="free_time",
                        notes="最終受付翌2:00／税込2 970円",
                        drink_option="1ドリンク制"
                    ),
                    PlanOption(
                        days=["sat","sun","holiday"],
                        customer_type="member",
                        amount=3_000,
                        unit_type="free_time",
                        notes="最終受付翌2:00／税込3 300円",
                        drink_option="1ドリンク制"
                    ),
                ],
            ),
            # 夜まふ（18:00～5:00・23:00～5:00／学生限定）
            PricingPlan(
                plan_name="まふ",
                start_time="18:00",
                end_time="05:00",
                options=[
                    PlanOption(
                        days=["mon","tue","wed","thu","fri"],
                        customer_type="member",
                        amount=700,
                        unit_type="special",
                        notes="短大・大学生・専門学生対象／税込770円",
                        drink_option="ソフトドリンク飲み放題"
                    ),
                    PlanOption(
                        days=["sat","sun","holiday"],
                        customer_type="member",
                        amount=1_500,
                        unit_type="special",
                        notes="短大・大学生・専門学生対象／税込1 650円",
                        drink_option="ソフトドリンク飲み放題"
                    ),
                ],
            ),
        ],
        drink_type=["1ドリンク制", "ソフトドリンク飲み放題"]
    ),
    KaraokeStore(
        id=10,
        store_name="ビッグエコー 赤坂見附本店",
        latitude=35.676778,
        longitude=139.736802,
        phone_number="03-6234-6688",
        business_hours=[
            # 月～金 12:00～翌5:00
            BusinessHour(day_type=day, start_time="12:00", end_time="05:00")
            for day in ["mon","tue","wed","thu","fri","holiday_eve"]
        ] + [
            # 土・日・祝 11:00～翌5:00
            BusinessHour(day_type=day, start_time="11:00", end_time="05:00")
            for day in ["sat","sun","holiday"]
        ],
        tax_type="tax_included",  # 表示は税込料金のため
        chain_name="ビッグエコー",
        pricing_plans=[
            # 30分料金（OPEN～18:00）
            PricingPlan(
                plan_name="30分料金",
                start_time="12:00",
                end_time="18:00",
                options=[
                    # 平日
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="student", amount=180, unit_type="per_30min", drink_option="1ドリンク制") ,  # 学割180円 :contentReference[oaicite:4]{index=4}
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="member",  amount=250, unit_type="per_30min", drink_option="1ドリンク制"),  # 会員250円 :contentReference[oaicite:5]{index=5}
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="general", amount=360, unit_type="per_30min", drink_option="1ドリンク制"),  # 一般360円 :contentReference[oaicite:6]{index=6}
                    # 週末・祝
                    PlanOption(days=["sat","sun","holiday"], customer_type="student", amount=320, unit_type="per_30min", drink_option="1ドリンク制"),  # 学割320円 :contentReference[oaicite:7]{index=7}
                    PlanOption(days=["sat","sun","holiday"], customer_type="member",  amount=380, unit_type="per_30min", drink_option="1ドリンク制"),  # 会員380円 :contentReference[oaicite:8]{index=8}
                    PlanOption(days=["sat","sun","holiday"], customer_type="general", amount=550, unit_type="per_30min", drink_option="1ドリンク制"),  # 一般550円 :contentReference[oaicite:9]{index=9}
                ],
            ),
            # 30分料金（18:00～CLOSE）
            PricingPlan(
                plan_name="30分料金",
                start_time="18:00",
                end_time="05:00",
                options=[
                    # 月～木
                    PlanOption(days=["mon","tue","wed","thu"], customer_type="student", amount=500, unit_type="per_30min", drink_option="1ドリンク制"),  # 学割500円 :contentReference[oaicite:10]{index=10}
                    PlanOption(days=["mon","tue","wed","thu"], customer_type="member",  amount=600, unit_type="per_30min", drink_option="1ドリンク制"),  # 会員600円 :contentReference[oaicite:11]{index=11}
                    PlanOption(days=["mon","tue","wed","thu"], customer_type="general", amount=880, unit_type="per_30min", drink_option="1ドリンク制"),  # 一般880円 :contentReference[oaicite:12]{index=12}
                    # 金～日・祝・祝前日
                    PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="student", amount=500, unit_type="per_30min", drink_option="1ドリンク制"),  # 学割500円 :contentReference[oaicite:13]{index=13}
                    PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="member",  amount=700, unit_type="per_30min", drink_option="1ドリンク制"),  # 会員700円 :contentReference[oaicite:14]{index=14}
                    PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="general", amount=990, unit_type="per_30min", drink_option="1ドリンク制"),  # 一般990円 :contentReference[oaicite:15]{index=15}
                ],
            ),
            # 昼フリータイム（OPEN～18:00）
            PricingPlan(
                plan_name="フリータイム",
                start_time="12:00",
                end_time="18:00",
                options=[
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="student", amount=770, unit_type="free_time", drink_option="1ドリンク制"),  # 学割770円 :contentReference[oaicite:16]{index=16}
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="member",  amount=1100, unit_type="free_time", drink_option="1ドリンク制"),  # 会員1100円 :contentReference[oaicite:17]{index=17}
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="general", amount=1600, unit_type="free_time", drink_option="1ドリンク制"),  # 一般1600円 :contentReference[oaicite:18]{index=18}
                    PlanOption(days=["sat","sun","holiday"],         customer_type="student", amount=1280, unit_type="free_time", drink_option="1ドリンク制"),  # 学割1280円 :contentReference[oaicite:19]{index=19}
                    PlanOption(days=["sat","sun","holiday"],         customer_type="member",  amount=1780, unit_type="free_time", drink_option="1ドリンク制"),  # 会員1780円 :contentReference[oaicite:20]{index=20}
                    PlanOption(days=["sat","sun","holiday"],         customer_type="general", amount=2550, unit_type="free_time", drink_option="1ドリンク制"),  # 一般2550円 :contentReference[oaicite:21]{index=21}
                ],
            ),
            # 夕方フリータイム（15:00～20:00）
            PricingPlan(
                plan_name="夕方フリータイム",
                start_time="15:00",
                end_time="20:00",
                options=[
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="student", amount=1580, unit_type="free_time", drink_option="1ドリンク制"),  # 学割1580円 :contentReference[oaicite:22]{index=22}
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="member",  amount=1780, unit_type="free_time", drink_option="1ドリンク制"),  # 会員1780円 :contentReference[oaicite:23]{index=23}
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="general", amount=2550, unit_type="free_time", drink_option="1ドリンク制"),  # 一般2550円 :contentReference[oaicite:24]{index=24}
                    PlanOption(days=["sat","sun","holiday"],         customer_type="student", amount=1780, unit_type="free_time", drink_option="1ドリンク制"),  # 学割1780円 :contentReference[oaicite:25]{index=25}
                    PlanOption(days=["sat","sun","holiday"],         customer_type="member",  amount=2480, unit_type="free_time", drink_option="1ドリンク制"),  # 会員2480円 :contentReference[oaicite:26]{index=26}
                    PlanOption(days=["sat","sun","holiday"],         customer_type="general", amount=3750, unit_type="free_time", drink_option="1ドリンク制"),  # 一般3750円 :contentReference[oaicite:27]{index=27}
                ],
            ),
            # ロングフリータイム（18:00～CLOSE）
            PricingPlan(
                plan_name="ロングフリータイム",
                start_time="18:00",
                end_time="00:00",
                options=[
                    PlanOption(days=["mon","tue","wed","thu"], customer_type="student", amount=3000, unit_type="free_time", drink_option="1ドリンク制"),  # 学割3000円 :contentReference[oaicite:28]{index=28}
                    PlanOption(days=["mon","tue","wed","thu"], customer_type="member",  amount=3500, unit_type="free_time", drink_option="1ドリンク制"),  # 会員3500円 :contentReference[oaicite:29]{index=29}
                    PlanOption(days=["mon","tue","wed","thu"], customer_type="general", amount=4500, unit_type="free_time", drink_option="1ドリンク制"),  # 一般4500円 :contentReference[oaicite:30]{index=30}
                    PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="student", amount=3500, unit_type="free_time", drink_option="1ドリンク制"),  # 学割3500円 :contentReference[oaicite:31]{index=31}
                    PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="member",  amount=4400, unit_type="free_time", drink_option="1ドリンク制"),  # 会員4400円 :contentReference[oaicite:32]{index=32}
                    PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="general", amount=5000, unit_type="free_time", drink_option="1ドリンク制"),  # 一般5000円 :contentReference[oaicite:33]{index=33}
                ],
            ),
            # 深夜フリータイム（23:00～CLOSE） ※一般料金が未確認のため要ご提供
            PricingPlan(
                plan_name="深夜フリータイム",
                start_time="23:00",
                end_time="00:00",
                options=[
                    PlanOption(days=["mon","tue","wed","thu"], customer_type="student", amount=2500, unit_type="free_time", drink_option="1ドリンク制"),  # 学割2500円 :contentReference[oaicite:34]{index=34}
                    PlanOption(days=["mon","tue","wed","thu"], customer_type="member",  amount=2900, unit_type="free_time", drink_option="1ドリンク制"),  # 会員2900円 :contentReference[oaicite:35]{index=35}
                    # PlanOption(days=["mon","tue","wed","thu"], customer_type="general", amount=???, unit_type="free_time", drink_option="1ドリンク制"),
                    PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="student", amount=2500, unit_type="free_time", drink_option="1ドリンク制"),  # 学割2500円 :contentReference[oaicite:36]{index=36}
                    PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="member",  amount=3300, unit_type="free_time", drink_option="1ドリンク制"),  # 会員3300円 :contentReference[oaicite:37]{index=37}
                    # PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="general", amount=???, unit_type="free_time", drink_option="1ドリンク制"),
                ],
            ),
        ],
        drink_type=["1ドリンク制"]
    ),
    KaraokeStore(
        id=11,
        store_name="ビッグエコー 新橋SL広場駅前店",
        latitude=35.667144,
        longitude=139.756320,
        phone_number="03-3580-6735",
        business_hours=[
            # 月〜金・祝前日 11:00〜翌5:00
            BusinessHour(day_type=day, start_time="11:00", end_time="05:00")
            for day in ["mon", "tue", "wed", "thu", "fri", "holiday_eve"]
        ] + [
            # 土曜日 11:00〜翌5:00
            BusinessHour(day_type="sat", start_time="11:00", end_time="05:00")
        ] + [
            # 日曜・祝祭日 11:00〜翌1:00
            BusinessHour(day_type=day, start_time="11:00", end_time="01:00")
            for day in ["sun", "holiday"]
        ],
        tax_type="tax_included",
        chain_name="ビッグエコー",
        pricing_plans=[
            # 30分料金（11:00〜18:00）【1ドリンクオーダー制】
            PricingPlan(
                plan_name="30分料金",
                start_time="11:00",
                end_time="18:00",
                options=[
                    PlanOption(days=["mon","tue","wed","thu","fri"],
                            customer_type="student", amount=100,
                            unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["mon","tue","wed","thu","fri"],
                            customer_type="member", amount=140,
                            unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["mon","tue","wed","thu","fri"],
                            customer_type="general", amount=190,
                            unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["sat","sun","holiday"],
                            customer_type="student", amount=190,
                            unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["sat","sun","holiday"],
                            customer_type="member", amount=330,
                            unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["sat","sun","holiday"],
                            customer_type="general", amount=220,
                            unit_type="per_30min", drink_option="1ドリンク制"),
                ],
            ),
            # 30分料金（18:00〜CLOSE）【1ドリンクオーダー制】
            PricingPlan(
                plan_name="30分料金",
                start_time="18:00",
                end_time="05:00",
                options=[
                    PlanOption(days=["mon","tue","wed","thu"],
                            customer_type="student", amount=400,
                            unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["mon","tue","wed","thu"],
                            customer_type="member", amount=680,
                            unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["mon","tue","wed","thu"],
                            customer_type="general", amount=980,
                            unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["fri","sat","sun","holiday","holiday_eve"],
                            customer_type="student", amount=460,
                            unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["fri","sat","sun","holiday","holiday_eve"],
                            customer_type="member", amount=740,
                            unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["fri","sat","sun","holiday","holiday_eve"],
                            customer_type="general", amount=1060,
                            unit_type="per_30min", drink_option="1ドリンク制"),
                ],
            ),
            # フリータイム（11:00〜19:00）【1ドリンクオーダー制】
            PricingPlan(
                plan_name="フリータイム",
                start_time="11:00",
                end_time="19:00",
                options=[
                    PlanOption(days=["mon","tue","wed","thu","fri"],
                            customer_type="student", amount=500,
                            unit_type="free_time", drink_option="1ドリンク制"),
                    PlanOption(days=["mon","tue","wed","thu","fri"],
                            customer_type="member", amount=750,
                            unit_type="free_time", drink_option="1ドリンク制"),
                    PlanOption(days=["mon","tue","wed","thu","fri"],
                            customer_type="general", amount=1000,
                            unit_type="free_time", drink_option="1ドリンク制"),
                    PlanOption(days=["sat","sun","holiday"],
                            customer_type="student", amount=950,
                            unit_type="free_time", drink_option="1ドリンク制"),
                    PlanOption(days=["sat","sun","holiday"],
                            customer_type="member", amount=1100,
                            unit_type="free_time", drink_option="1ドリンク制"),
                    PlanOption(days=["sat","sun","holiday"],
                            customer_type="general", amount=1600,
                            unit_type="free_time", drink_option="1ドリンク制"),
                ],
            ),
            # 深夜フリータイム（23:00〜5:00）【1ドリンクオーダー制】
            PricingPlan(
                plan_name="深夜フリータイム",
                start_time="23:00",
                end_time="05:00",
                options=[
                    PlanOption(days=["mon","tue","wed","thu"],
                            customer_type="student", amount=1800,
                            unit_type="free_time", drink_option="1ドリンク制"),
                    PlanOption(days=["mon","tue","wed","thu"],
                            customer_type="member", amount=2400,
                            unit_type="free_time", drink_option="1ドリンク制"),
                    PlanOption(days=["mon","tue","wed","thu"],
                            customer_type="general", amount=4000,
                            unit_type="free_time", drink_option="1ドリンク制"),
                    PlanOption(days=["fri","sat","sun","holiday","holiday_eve"],
                            customer_type="student", amount=2000,
                            unit_type="free_time", drink_option="1ドリンク制"),
                    PlanOption(days=["fri","sat","sun","holiday","holiday_eve"],
                            customer_type="member", amount=3000,
                            unit_type="free_time", drink_option="1ドリンク制"),
                    PlanOption(days=["fri","sat","sun","holiday","holiday_eve"],
                            customer_type="general", amount=5000,
                            unit_type="free_time", drink_option="1ドリンク制"),
                ],
            ),
        ],
        drink_type=["1ドリンク制"]
    ),
    KaraokeStore(
        id=12,
        store_name="ビッグエコー 新橋烏森口店",
        latitude=35.66578,
        longitude=139.757417,
        phone_number="03-6402-4170",
        business_hours=[
            # 月～木・祝前日 11:00～翌5:00
            BusinessHour(day_type=day, start_time="11:00", end_time="05:00")
            for day in ["mon", "tue", "wed", "thu", "holiday_eve"]
        ] + [
            # 金曜日 11:00～翌7:00
            BusinessHour(day_type="fri", start_time="11:00", end_time="07:00"),
            # 土曜日 10:00～翌7:00
            BusinessHour(day_type="sat", start_time="10:00", end_time="07:00")
        ] + [
            # 日曜・祝祭日 10:00～翌5:00
            BusinessHour(day_type=day, start_time="10:00", end_time="05:00")
            for day in ["sun", "holiday"]
        ],
        tax_type="tax_included",
        chain_name="ビッグエコー",
        pricing_plans=[
            # 30分料金（11:00～18:00）
            PricingPlan(
                plan_name="30分料金",
                start_time="11:00",
                end_time="18:00",
                options=[
                    PlanOption(days=["mon","tue","wed","thu","holiday_eve"], customer_type="student", amount=100, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                    PlanOption(days=["mon","tue","wed","thu","holiday_eve"], customer_type="member",  amount=140, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                    PlanOption(days=["mon","tue","wed","thu","holiday_eve"], customer_type="general", amount=190, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                    PlanOption(days=["sat","sun","holiday"],                      customer_type="student", amount=190, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                    PlanOption(days=["sat","sun","holiday"],                      customer_type="member",  amount=330, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                    PlanOption(days=["sat","sun","holiday"],                      customer_type="general", amount=220, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                ],
            ),
            # 30分料金（18:00～CLOSE）
            PricingPlan(
                plan_name="30分料金",
                start_time="18:00",
                end_time="05:00",
                options=[
                    PlanOption(days=["mon","tue","wed","thu"],                customer_type="student", amount=400, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                    PlanOption(days=["mon","tue","wed","thu"],                customer_type="member",  amount=680, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                    PlanOption(days=["mon","tue","wed","thu"],                customer_type="general", amount=980, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                    PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="student", amount=460, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                    PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="member",  amount=740, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                    PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="general", amount=1060,unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                ],
            ),
            # フリータイム（11:00～19:00）
            PricingPlan(
                plan_name="フリータイム",
                start_time="11:00",
                end_time="19:00",
                options=[
                    PlanOption(days=["mon","tue","wed","thu","holiday_eve"], customer_type="student", amount=500,  unit_type="free_time", drink_option="1ドリンクオーダー制"),
                    PlanOption(days=["mon","tue","wed","thu","holiday_eve"], customer_type="member",  amount=750,  unit_type="free_time", drink_option="1ドリンクオーダー制"),
                    PlanOption(days=["mon","tue","wed","thu","holiday_eve"], customer_type="general", amount=1000, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                    PlanOption(days=["sat","sun","holiday"],                   customer_type="student", amount=950,  unit_type="free_time", drink_option="1ドリンクオーダー制"),
                    PlanOption(days=["sat","sun","holiday"],                   customer_type="member",  amount=1100, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                    PlanOption(days=["sat","sun","holiday"],                   customer_type="general", amount=1600, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                ],
            ),
            # 深夜フリータイム（23:00～5:00）
            PricingPlan(
                plan_name="深夜フリータイム",
                start_time="23:00",
                end_time="05:00",
                options=[
                    PlanOption(days=["mon","tue","wed","thu"],                customer_type="student", amount=1800, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                    PlanOption(days=["mon","tue","wed","thu"],                customer_type="member",  amount=2400, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                    PlanOption(days=["mon","tue","wed","thu"],                customer_type="general", amount=4000, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                    PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="student", amount=2000, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                    PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="member",  amount=3000, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                    PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="general", amount=5000, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                ],
            ),
        ],
        drink_type=["1ドリンクオーダー制"]
    ),
    KaraokeStore(
    id=13,
    store_name="カラオケ ビッグエコー 新橋銀座口駅前店",
    latitude=35.667505,
    longitude=139.758770,
    phone_number="03-3289-8800",
    business_hours=[
        # 月～木 11:00～翌5:00
        BusinessHour(day_type=day, start_time="11:00", end_time="05:00")
        for day in ["mon", "tue", "wed", "thu"]
    ] + [
        # 金・祝前日 11:00～翌7:00
        BusinessHour(day_type=day, start_time="11:00", end_time="07:00")
        for day in ["fri", "holiday_eve"]
    ] + [
        # 土 10:00～翌7:00
        BusinessHour(day_type="sat", start_time="10:00", end_time="07:00")
    ] + [
        # 日・祝日 10:00～翌5:00
        BusinessHour(day_type=day, start_time="10:00", end_time="05:00")
        for day in ["sun", "holiday"]
    ],
    tax_type="tax_included",
    chain_name="ビッグエコー",
    pricing_plans=[
        # 30分料金（OPEN～18:00）
        PricingPlan(
            plan_name="30分料金",
            start_time="11:00",
            end_time="18:00",
            options=[
                PlanOption(days=["mon","tue","wed","thu","holiday_eve"], customer_type="student", amount=150, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["mon","tue","wed","thu","holiday_eve"], customer_type="senior",  amount=150, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["mon","tue","wed","thu","holiday_eve"], customer_type="member",  amount=220, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["mon","tue","wed","thu","holiday_eve"], customer_type="general", amount=320, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["mon","tue","wed","thu","holiday_eve"], customer_type="member",  amount=300, unit_type="per_30min", notes="ひとりカラオケ料金", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["sat","sun","holiday"],                  customer_type="student", amount=180, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["sat","sun","holiday"],                  customer_type="senior",  amount=180, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["sat","sun","holiday"],                  customer_type="member",  amount=250, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["sat","sun","holiday"],                  customer_type="general", amount=360, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["sat","sun","holiday"],                  customer_type="member",  amount=350, unit_type="per_30min", notes="ひとりカラオケ料金", drink_option="1ドリンクオーダー制"),
            ],
        ),
        # 30分料金（18:00～CLOSE）
        PricingPlan(
            plan_name="30分料金",
            start_time="18:00",
            end_time="05:00",
            options=[
                PlanOption(days=["mon","tue","wed","thu"],                customer_type="student", amount=400, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["mon","tue","wed","thu"],                customer_type="senior",  amount=400, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["mon","tue","wed","thu"],                customer_type="member",  amount=680, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["mon","tue","wed","thu"],                customer_type="general", amount=980, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["mon","tue","wed","thu"],                customer_type="member",  amount=740, unit_type="per_30min", notes="ひとりカラオケ料金", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="student", amount=460, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="senior",  amount=460, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="member",  amount=740, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="general", amount=1060,unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="member",  amount=810, unit_type="per_30min", notes="ひとりカラオケ料金", drink_option="1ドリンクオーダー制"),
            ],
        ),
        # 昼フリータイム（OPEN～19:00）
        PricingPlan(
            plan_name="フリータイム",
            start_time="11:00",
            end_time="19:00",
            options=[
                PlanOption(days=["mon","tue","wed","thu","holiday_eve"], customer_type="student", amount=750,  unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["mon","tue","wed","thu","holiday_eve"], customer_type="senior",  amount=750,  unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["mon","tue","wed","thu","holiday_eve"], customer_type="member",  amount=1100, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["mon","tue","wed","thu","holiday_eve"], customer_type="general", amount=1600, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["sat","sun","holiday"],                   customer_type="student", amount=900,  unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["sat","sun","holiday"],                   customer_type="senior",  amount=900,  unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["sat","sun","holiday"],                   customer_type="member",  amount=1250, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["sat","sun","holiday"],                   customer_type="general", amount=1800, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["sat","sun","holiday"],                   customer_type="member",  amount=1750, unit_type="free_time", notes="ひとりカラオケ料金", drink_option="1ドリンクオーダー制"),
            ],
        ),
        # 夜フリータイム（23:00～翌5:00）
        PricingPlan(
            plan_name="深夜フリータイム",
            start_time="23:00",
            end_time="05:00",
            options=[
                PlanOption(days=["mon","tue","wed","thu"],                customer_type="student", amount=1800, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["mon","tue","wed","thu"],                customer_type="senior",  amount=1800, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["mon","tue","wed","thu"],                customer_type="member",  amount=2400, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["mon","tue","wed","thu"],                customer_type="general", amount=4000, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="student", amount=2000, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="senior",  amount=2000, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="member",  amount=3000, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="general", amount=5000, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["fri","sat","sun","holiday","holiday_eve"], customer_type="member",  amount=3500, unit_type="free_time", notes="ひとりカラオケ料金", drink_option="1ドリンクオーダー制"),
            ],
        ),
    ],
    drink_type=["1ドリンクオーダー制"]
),
    KaraokeStore(
    id=14,
    store_name="カラオケ ビッグエコー 銀座店",
    latitude=35.667697,
    longitude=139.759870,
    phone_number="03-5568-7788",
    business_hours=[
        # 月～木 20:00～翌5:00
        BusinessHour(day_type=day, start_time="20:00", end_time="05:00")
        for day in ["mon", "tue", "wed", "thu"]
    ] + [
        # 金・祝前日 18:00～翌6:00
        BusinessHour(day_type=day, start_time="18:00", end_time="06:00")
        for day in ["fri", "holiday_eve"]
    ] + [
        # 土 18:00～翌5:00
        BusinessHour(day_type="sat", start_time="18:00", end_time="05:00"),
        # 日・祝日 定休日
    ],
    tax_type="tax_included",
    chain_name="ビッグエコー",
    pricing_plans=[
        # 30分料金（OPEN～CLOSE）
        PricingPlan(
            plan_name="30分料金",
            start_time="00:00",
            end_time="00:00",
            options=[
                PlanOption(days=["mon","tue","wed","thu"], customer_type="student", amount=400, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["mon","tue","wed","thu"], customer_type="senior",  amount=400, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["mon","tue","wed","thu"], customer_type="member",  amount=680, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["mon","tue","wed","thu"], customer_type="general", amount=980, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["mon","tue","wed","thu"], customer_type="member",  amount=740, unit_type="per_30min", notes="ひとりカラオケ料金", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["fri","sat","holiday_eve"], customer_type="student", amount=460, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["fri","sat","holiday_eve"], customer_type="senior",  amount=460, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["fri","sat","holiday_eve"], customer_type="member",  amount=740, unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["fri","sat","holiday_eve"], customer_type="general", amount=1060,unit_type="per_30min", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["fri","sat","holiday_eve"], customer_type="member",  amount=810, unit_type="per_30min", notes="ひとりカラオケ料金", drink_option="1ドリンクオーダー制"),
            ],
        ),
        # 深夜フリータイム（23:00～CLOSE）
        PricingPlan(
            plan_name="深夜フリータイム",
            start_time="23:00",
            end_time="05:00",
            options=[
                PlanOption(days=["mon","tue","wed","thu"], customer_type="student", amount=2000, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["mon","tue","wed","thu"], customer_type="senior",  amount=2000, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["mon","tue","wed","thu"], customer_type="member",  amount=2400, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["mon","tue","wed","thu"], customer_type="general", amount=4000, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["fri","sat","holiday_eve"], customer_type="student", amount=2000, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["fri","sat","holiday_eve"], customer_type="senior",  amount=2000, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["fri","sat","holiday_eve"], customer_type="member",  amount=3000, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["fri","sat","holiday_eve"], customer_type="general", amount=5000, unit_type="free_time", drink_option="1ドリンクオーダー制"),
                PlanOption(days=["fri","sat","holiday_eve"], customer_type="member",  amount=3500, unit_type="free_time", notes="ひとりカラオケ料金", drink_option="1ドリンクオーダー制"),
            ],
        ),
    ],
    drink_type=["1ドリンクオーダー制"]
),
    KaraokeStore(
        id=15,
        store_name="カラオケの鉄人 新橋SL広場前店",
        latitude=35.666641,
        longitude=139.756828,
        phone_number="03-6273-3484",
        business_hours=[
            # 月〜木・日・祝 12:00〜翌6:00
            BusinessHour(day_type=day, start_time="12:00", end_time="06:00")
            for day in ["mon", "tue", "wed", "thu", "sun", "holiday"]
        ] + [
            # 金・土・祝前日 12:00〜翌8:00
            BusinessHour(day_type=day, start_time="12:00", end_time="08:00")
            for day in ["fri", "sat", "holiday_eve"]
        ],
        tax_type="tax_included",
        chain_name="カラオケの鉄人",
        pricing_plans=[
            # 室料30分（OPEN〜18:00）
            PricingPlan(
                plan_name="室料30分",
                start_time="12:00",
                end_time="18:00",
                options=[
                    PlanOption(
                        days=["mon","tue","wed","thu","fri"],
                        customer_type="member",
                        amount=100,
                        unit_type="per_30min",
                        drink_option="ワンドリンクオーダー制"
                    ),
                    PlanOption(
                        days=["mon","tue","wed","thu","fri"],
                        customer_type="general",
                        amount=142,
                        unit_type="per_30min",
                        drink_option="ワンドリンクオーダー制"
                    ),
                    PlanOption(
                        days=["sat","sun","holiday"],
                        customer_type="member",
                        amount=160,
                        unit_type="per_30min",
                        drink_option="ワンドリンクオーダー制"
                    ),
                    PlanOption(
                        days=["sat","sun","holiday"],
                        customer_type="general",
                        amount=227,
                        unit_type="per_30min",
                        drink_option="ワンドリンクオーダー制"
                    ),
                ],
            ),
            # フリータイム（OPEN〜20:00）
            PricingPlan(
                plan_name="フリータイム",
                start_time="12:00",
                end_time="20:00",
                options=[
                    PlanOption(
                        days=["mon","tue","wed","thu","fri"],
                        customer_type="member",
                        amount=1200,
                        unit_type="free_time",
                        drink_option="ドリンクバー付"
                    ),
                    PlanOption(
                        days=["mon","tue","wed","thu","fri"],
                        customer_type="general",
                        amount=1704,
                        unit_type="free_time",
                        drink_option="ドリンクバー付"
                    ),
                    PlanOption(
                        days=["sat","sun","holiday"],
                        customer_type="member",
                        amount=1700,
                        unit_type="free_time",
                        drink_option="ドリンクバー付"
                    ),
                    PlanOption(
                        days=["sat","sun","holiday"],
                        customer_type="general",
                        amount=2414,
                        unit_type="free_time",
                        drink_option="ドリンクバー付"
                    ),
                ],
            ),
            # 室料30分（18:00〜翌6:00）
            PricingPlan(
                plan_name="室料30分",
                start_time="18:00",
                end_time="06:00",
                options=[
                    PlanOption(
                        days=["sun","mon","tue","wed","thu"],
                        customer_type="member",
                        amount=650,
                        unit_type="per_30min",
                        drink_option="ワンドリンクオーダー制"
                    ),
                    PlanOption(
                        days=["sun","mon","tue","wed","thu"],
                        customer_type="general",
                        amount=923,
                        unit_type="per_30min",
                        drink_option="ワンドリンクオーダー制"
                    ),
                    PlanOption(
                        days=["fri","sat","holiday_eve"],
                        customer_type="member",
                        amount=720,
                        unit_type="per_30min",
                        drink_option="ワンドリンクオーダー制"
                    ),
                    PlanOption(
                        days=["fri","sat","holiday_eve"],
                        customer_type="general",
                        amount=1022,
                        unit_type="per_30min",
                        drink_option="ワンドリンクオーダー制"
                    ),
                ],
            ),
            # 深夜フリータイム（22:00〜翌5:00）
            PricingPlan(
                plan_name="深夜フリータイム",
                start_time="22:00",
                end_time="05:00",
                options=[
                    PlanOption(
                        days=["mon","tue","wed","thu"],
                        customer_type="general",
                        amount=700,
                        unit_type="free_time",
                        drink_option="ドリンクバー無料"
                    ),
                    PlanOption(
                        days=["fri","sat","sun","holiday","holiday_eve"],
                        customer_type="general",
                        amount=2000,
                        unit_type="free_time",
                        drink_option="ドリンクバー無料"
                    ),
                ],
            ),
        ],
        drink_type=["ワンドリンクオーダー制", "ドリンクバー付"]
    ),
    KaraokeStore(
        id=16,
        store_name="カラオケパセラ 赤坂店",
        latitude=35.673293,
        longitude=139.737676,
        phone_number="0120-759-926",
        business_hours=[
            # 月〜金・祝前日 17:00〜翌5:00
            BusinessHour(day_type=day, start_time="17:00", end_time="05:00")
            for day in ["mon", "tue", "wed", "thu", "fri", "holiday_eve"]
        ] + [
            # 土曜 11:00〜翌5:00
            BusinessHour(day_type="sat", start_time="11:00", end_time="05:00")
        ] + [
            # 日曜・祝日 11:00〜23:00
            BusinessHour(day_type=day, start_time="11:00", end_time="23:00")
            for day in ["sun", "holiday"]
        ],
        tax_type="tax_included",
        chain_name="パセラ",
        pricing_plans=[
            # 基本30分料金（OPEN〜17:00）
            PricingPlan(
                plan_name="30分料金",
                start_time="00:00",
                end_time="17:00",
                options=[
                    PlanOption(
                        days=["mon","tue","wed","thu","fri","sat","sun","holiday","holiday_eve"],
                        customer_type="member",
                        amount=580,
                        unit_type="per_30min",
                        drink_option="1ドリンク付き（アルコール含む）"
                    ),
                    PlanOption(
                        days=["mon","tue","wed","thu","fri","sat","sun","holiday","holiday_eve"],
                        customer_type="general",
                        amount=580,
                        unit_type="per_30min",
                        drink_option="1ドリンク付き（アルコール含む）"
                    ),
                ],
            ),
            # 基本30分料金（17:00〜CLOSE）
            PricingPlan(
                plan_name="30分料金",
                start_time="17:00",
                end_time="00:00",
                options=[
                    PlanOption(
                        days=["mon","tue","wed","thu"],
                        customer_type="member",
                        amount=780,
                        unit_type="per_30min",
                        drink_option="1ドリンク付き（アルコール含む）"
                    ),
                    PlanOption(
                        days=["mon","tue","wed","thu"],
                        customer_type="general",
                        amount=780,
                        unit_type="per_30min",
                        drink_option="1ドリンク付き（アルコール含む）"
                    ),
                    PlanOption(
                        days=["fri","sat","sun","holiday","holiday_eve"],
                        customer_type="member",
                        amount=880,
                        unit_type="per_30min",
                        drink_option="1ドリンク付き（アルコール含む）"
                    ),
                    PlanOption(
                        days=["fri","sat","sun","holiday","holiday_eve"],
                        customer_type="general",
                        amount=880,
                        unit_type="per_30min",
                        drink_option="1ドリンク付き（アルコール含む）"
                    ),
                ],
            ),
            # デイタイムパック（ソフトドリンク飲み放題付き）
            PricingPlan(
                plan_name="デイタイムパック",
                start_time="00:00",
                end_time="17:00",
                options=[
                    PlanOption(
                        days=["mon","tue","wed","thu","fri"],
                        customer_type="member",
                        amount=2980,
                        unit_type="special",
                        notes="3時間パック",
                        drink_option="ソフトドリンク飲み放題"
                    ),
                    PlanOption(
                        days=["mon","tue","wed","thu","fri"],
                        customer_type="member",
                        amount=4480,
                        unit_type="special",
                        notes="5時間パック",
                        drink_option="ソフトドリンク飲み放題"
                    ),
                    PlanOption(
                        days=["sat","sun","holiday"],
                        customer_type="member",
                        amount=3980,
                        unit_type="special",
                        notes="3時間パック",
                        drink_option="ソフトドリンク飲み放題"
                    ),
                    PlanOption(
                        days=["sat","sun","holiday"],
                        customer_type="member",
                        amount=5980,
                        unit_type="special",
                        notes="5時間パック",
                        drink_option="ソフトドリンク飲み放題"
                    ),
                ],
            ),
            # ハッピーアワーパック（アルコール含む1ドリンク付き）
            PricingPlan(
                plan_name="ハッピーアワーパック",
                start_time="16:00",
                end_time="20:00",
                options=[
                    PlanOption(
                        days=["mon","tue","wed","thu"],
                        customer_type="member",
                        amount=1980,
                        unit_type="special",
                        drink_option="アルコール含む1ドリンク"
                    ),
                    PlanOption(
                        days=["fri","sat","sun","holiday_eve"],
                        customer_type="member",
                        amount=3980,
                        unit_type="special",
                        drink_option="アルコール含む1ドリンク"
                    ),
                ],
            ),
            # パセラパーティーパック（スタンダード飲み放題付き）
            PricingPlan(
                plan_name="パセラパーティーパック",
                start_time="00:00",
                end_time="00:00",
                options=[
                    PlanOption(
                        days=["mon","tue","wed","thu"],
                        customer_type="member",
                        amount=4800,
                        unit_type="special",
                        notes="2時間パック",
                        drink_option="スタンダード飲み放題"
                    ),
                    PlanOption(
                        days=["mon","tue","wed","thu"],
                        customer_type="member",
                        amount=5800,
                        unit_type="special",
                        notes="3時間パック",
                        drink_option="スタンダード飲み放題"
                    ),
                    PlanOption(
                        days=["fri","sat","sun","holiday","holiday_eve"],
                        customer_type="member",
                        amount=5300,
                        unit_type="special",
                        notes="2時間パック",
                        drink_option="スタンダード飲み放題"
                    ),
                    PlanOption(
                        days=["fri","sat","sun","holiday","holiday_eve"],
                        customer_type="member",
                        amount=6300,
                        unit_type="special",
                        notes="3時間パック",
                        drink_option="スタンダード飲み放題"
                    ),
                ],
            ),
            # オールナイトフリータイム（22:00〜翌5:00）
            PricingPlan(
                plan_name="オールナイトフリータイム",
                start_time="22:00",
                end_time="05:00",
                options=[
                    PlanOption(
                        days=["mon","tue","wed","thu"],
                        customer_type="member",
                        amount=4000,
                        unit_type="free_time",
                        drink_option="ドリンクバー（無料）"
                    ),
                    PlanOption(
                        days=["fri","sat","sun","holiday","holiday_eve"],
                        customer_type="member",
                        amount=4500,
                        unit_type="free_time",
                        drink_option="ドリンクバー（無料）"
                    ),
                ],
            ),
        ],
        drink_type=[
            "1ドリンク付き（アルコール含む）",
            "ソフトドリンク飲み放題",
            "スタンダード飲み放題",
            "最上級プレミアム飲み放題",
            "ドリンクバー（無料）"
        ]
    ),
    KaraokeStore(
        id=17,
        store_name="カラオケ館 渋谷東口店",
        latitude=35.6590,       # 近隣店舗の平均座標を参考推定
        longitude=139.7010,     # 近隣店舗の平均座標を参考推定
        phone_number="03-5485-5757",
        business_hours=[
            # 日～木・祝 11:00～翌5:00
            BusinessHour(day_type=day, start_time="11:00", end_time="05:00")
            for day in ["sun","mon","tue","wed","thu","holiday"]
        ] + [
            # 金・土・祝前日 11:00～翌6:00
            BusinessHour(day_type=day, start_time="11:00", end_time="06:00")
            for day in ["fri","sat","holiday_eve"]
        ],
        tax_type="tax_included",
        chain_name="カラオケ館",
        pricing_plans=[
            PricingPlan(
                plan_name="30分料金",
                start_time="11:00",
                end_time="18:00",
                options=[
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="student", amount=210, unit_type="per_30min", drink_option="ドリンクバー付"),
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="member",  amount=210, unit_type="per_30min", drink_option="ドリンクバー付"),
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="general", amount=280, unit_type="per_30min", drink_option="ドリンクバー付"),
                    PlanOption(days=["sat","sun","holiday"],             customer_type="student", amount=330, unit_type="per_30min", drink_option="ドリンクバー付"),
                    PlanOption(days=["sat","sun","holiday"],             customer_type="member",  amount=330, unit_type="per_30min", drink_option="ドリンクバー付"),
                    PlanOption(days=["sat","sun","holiday"],             customer_type="general", amount=440, unit_type="per_30min", drink_option="ドリンクバー付"),
                ],
            ),
            PricingPlan(
                plan_name="30分料金",
                start_time="18:00",
                end_time="05:00",
                options=[
                    PlanOption(days=["sun","mon","tue","wed","thu"], customer_type="student", amount=390, unit_type="per_30min", drink_option="ドリンクバー付"),
                    PlanOption(days=["sun","mon","tue","wed","thu"], customer_type="member",  amount=480, unit_type="per_30min", drink_option="ドリンクバー付"),
                    PlanOption(days=["sun","mon","tue","wed","thu"], customer_type="general", amount=640, unit_type="per_30min", drink_option="ドリンクバー付"),
                    PlanOption(days=["fri","sat","holiday_eve"],      customer_type="student", amount=490, unit_type="per_30min", drink_option="ドリンクバー付"),
                    PlanOption(days=["fri","sat","holiday_eve"],      customer_type="member",  amount=600, unit_type="per_30min", drink_option="ドリンクバー付"),
                    PlanOption(days=["fri","sat","holiday_eve"],      customer_type="general", amount=800, unit_type="per_30min", drink_option="ドリンクバー付"),
                ],
            ),
            PricingPlan(
                plan_name="フリータイム",
                start_time="11:00",
                end_time="19:00",
                options=[
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="student", amount=1260, unit_type="free_time", drink_option="ドリンクバー付"),
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="member",  amount=1260, unit_type="free_time", drink_option="ドリンクバー付"),
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="general", amount=1680, unit_type="free_time", drink_option="ドリンクバー付"),
                    PlanOption(days=["sat","sun","holiday"],             customer_type="student", amount=1980, unit_type="free_time", drink_option="ドリンクバー付"),
                    PlanOption(days=["sat","sun","holiday"],             customer_type="member",  amount=1980, unit_type="free_time", drink_option="ドリンクバー付"),
                    PlanOption(days=["sat","sun","holiday"],             customer_type="general", amount=2640, unit_type="free_time", drink_option="ドリンクバー付"),
                ],
            ),
            PricingPlan(
                plan_name="深夜フリータイム",
                start_time="23:00",
                end_time="05:00",
                options=[
                    PlanOption(days=["sun","mon","tue","wed","thu"], customer_type="student", amount=1100, unit_type="free_time", drink_option="ドリンクバー付"),
                    PlanOption(days=["sun","mon","tue","wed","thu"], customer_type="member",  amount=1980, unit_type="free_time", drink_option="ドリンクバー付"),
                    PlanOption(days=["sun","mon","tue","wed","thu"], customer_type="general", amount=2640, unit_type="free_time", drink_option="ドリンクバー付"),
                    PlanOption(days=["fri","sat","holiday_eve"],      customer_type="student", amount=1980, unit_type="free_time", drink_option="ドリンクバー付"),
                    PlanOption(days=["fri","sat","holiday_eve"],      customer_type="member",  amount=2820, unit_type="free_time", drink_option="ドリンクバー付"),
                    PlanOption(days=["fri","sat","holiday_eve"],      customer_type="general", amount=3760, unit_type="free_time", drink_option="ドリンクバー付"),
                ],
            ),
            PricingPlan(
                plan_name="終電パック",
                start_time="18:00",
                end_time="00:00",
                options=[
                    PlanOption(days=["mon","tue","wed","thu","fri","sat","holiday_eve","sun","holiday"], customer_type="general", amount=1400, unit_type="special", notes="2.5時間分の料金で終電まで歌える", drink_option="1ドリンク制"),
                ],
            ),
            PricingPlan(
                plan_name="ロングフリータイム（学生限定）",
                start_time="18:00",
                end_time="05:00",
                options=[
                    PlanOption(days=["sun","mon","tue","wed","thu","holiday"], customer_type="student", amount=1100, unit_type="free_time", drink_option="ドリンクバー付"),
                    PlanOption(days=["fri","sat","holiday_eve"], customer_type="student", amount=1980, unit_type="free_time", drink_option="ドリンクバー付"),
                ],
            ),
        ],
        drink_type=["ドリンクバー付", "1ドリンク制"]
    ),
    KaraokeStore(
        id=18,
        store_name="カラオケ館 渋谷本店",
        latitude=35.660459,
        longitude=139.698826,
        phone_number="03-5728-6430",
        business_hours=[
            # 日～木・祝  9:00～翌5:00
            BusinessHour(day_type=day, start_time="09:00", end_time="05:00")
            for day in ["sun","mon","tue","wed","thu","holiday"]
        ] + [
            # 金・土・祝前日 9:00～翌7:00
            BusinessHour(day_type=day, start_time="09:00", end_time="07:00")
            for day in ["fri","sat","holiday_eve"]
        ],
        tax_type="tax_included",
        chain_name="カラオケ館",
        pricing_plans=[
            PricingPlan(
                plan_name="30分料金",
                start_time="09:00",
                end_time="18:00",
                options=[
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="student", amount=190, unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="member",  amount=190, unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="general", amount=253, unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["sat","sun","holiday"],             customer_type="student", amount=280, unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["sat","sun","holiday"],             customer_type="member",  amount=330, unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["sat","sun","holiday"],             customer_type="general", amount=440, unit_type="per_30min", drink_option="1ドリンク制"),
                ],
            ),
            PricingPlan(
                plan_name="30分料金",
                start_time="18:00",
                end_time="05:00",
                options=[
                    PlanOption(days=["sun","mon","tue","wed","thu"], customer_type="student", amount=350, unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["sun","mon","tue","wed","thu"], customer_type="member",  amount=460, unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["sun","mon","tue","wed","thu"], customer_type="general", amount=613, unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["fri","sat","holiday_eve"],      customer_type="student", amount=450, unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["fri","sat","holiday_eve"],      customer_type="member",  amount=570, unit_type="per_30min", drink_option="1ドリンク制"),
                    PlanOption(days=["fri","sat","holiday_eve"],      customer_type="general", amount=760, unit_type="per_30min", drink_option="1ドリンク制"),
                ],
            ),
            PricingPlan(
                plan_name="フリータイム",
                start_time="11:00",
                end_time="19:00",
                options=[
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="student", amount=980,  unit_type="free_time", drink_option="ドリンクバー付"),
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="member",  amount=1200, unit_type="free_time", drink_option="ドリンクバー付"),
                    PlanOption(days=["mon","tue","wed","thu","fri"], customer_type="general", amount=1600, unit_type="free_time", drink_option="ドリンクバー付"),
                    PlanOption(days=["sat","sun","holiday"],             customer_type="student", amount=1580, unit_type="free_time", drink_option="ドリンクバー付"),
                    PlanOption(days=["sat","sun","holiday"],             customer_type="member",  amount=1980, unit_type="free_time", drink_option="ドリンクバー付"),
                    PlanOption(days=["sat","sun","holiday"],             customer_type="general", amount=2640, unit_type="free_time", drink_option="ドリンクバー付"),
                ],
            ),
            PricingPlan(
                plan_name="深夜フリータイム",
                start_time="23:00",
                end_time="05:00",
                options=[
                    PlanOption(days=["sun","mon","tue","wed","thu"], customer_type="student", amount=1100, unit_type="free_time", drink_option="ドリンクバー付"),
                    PlanOption(days=["sun","mon","tue","wed","thu"], customer_type="member",  amount=1650, unit_type="free_time", drink_option="ドリンクバー付"),
                    PlanOption(days=["sun","mon","tue","wed","thu"], customer_type="general", amount=2200, unit_type="free_time", drink_option="ドリンクバー付"),
                    PlanOption(days=["fri","sat","holiday_eve"],      customer_type="student", amount=1980, unit_type="free_time", drink_option="ドリンクバー付"),
                    PlanOption(days=["fri","sat","holiday_eve"],      customer_type="member",  amount=2760, unit_type="free_time", drink_option="ドリンクバー付"),
                    PlanOption(days=["fri","sat","holiday_eve"],      customer_type="general", amount=3680, unit_type="free_time", drink_option="ドリンクバー付"),
                ],
            ),
            PricingPlan(
                plan_name="終電パック",
                start_time="18:00",
                end_time="00:00",
                options=[
                    PlanOption(days=["mon","tue","wed","thu","fri","sat","sun","holiday","holiday_eve"], customer_type="general", amount=280*5, unit_type="special", notes="2.5時間分の料金で終電まで歌える", drink_option="1ドリンク制"),
                ],
            ),
            PricingPlan(
                plan_name="ロングフリータイム（学生限定）",
                start_time="18:00",
                end_time="05:00",
                options=[
                    PlanOption(days=["sun","mon","tue","wed","thu","holiday"], customer_type="student", amount=1100, unit_type="free_time", drink_option="ドリンクバー付"),
                    PlanOption(days=["fri","sat","holiday_eve"], customer_type="student", amount=1980, unit_type="free_time", drink_option="ドリンクバー付"),
                ],
            ),
        ],
        drink_type=["1ドリンク制", "ドリンクバー付"]
    ),
]
