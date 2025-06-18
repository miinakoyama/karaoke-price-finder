from datetime import datetime, time
import math

class TimeRange:
    def __init__(self, start, end, unit, price_per_hour=None, price_total=None):
        self.start = start
        self.end = end
        self.unit = unit
        self.price_per_hour = price_per_hour
        self.price_total = price_total

class PricingRule:
    def __init__(self, customer_types, days, time_ranges):
        self.customer_types = customer_types
        self.days = days
        self.time_ranges = time_ranges

class Store:
    def __init__(self, name, lat, lon, phone,open_hour,rules,attribute):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.phone = phone
        self.open_hour = open_hour
        self.rules = rules
        self.attribute = attribute

def get_weekday_str(dt):
    return dt.strftime("%a").lower()  # e.g., 'mon', 'tue', etc.

def parse_time_str(s):
    return datetime.strptime(s, "%H:%M").time()

def is_within_time_range(start_str, end_str, dt):
    start = parse_time_str(start_str)
    end = parse_time_str(end_str)
    target_time = dt.time()

    if start < end:
        return start <= target_time < end
    else:
        return target_time >= start or target_time < end

def contains(lst, target):
    return target in lst

def find_cheapest_plan(rules, dt, isMember, isStudent, stay_minutes):
    day = get_weekday_str(dt)
    best_price = float('inf')
    best_type = ""
    found = False

    types_to_check = []
    if isMember:
        types_to_check.append("member")
    if isStudent:
        types_to_check.append("student")
    if not types_to_check:
        types_to_check.append("general")

    for rule in rules:
        if not any(ct in rule.customer_types for ct in types_to_check):
            continue
        if day not in rule.days:
            continue

        for tr in rule.time_ranges:
            if not is_within_time_range(tr.start, tr.end, dt):
                continue

            if tr.unit == "free_time":
                price = tr.price_total
            elif tr.unit == "per_30_min":
                units = math.ceil(stay_minutes / 30)
                price = tr.price_per_hour * units
            else:
                continue

            if price < best_price:
                best_price = price
                best_type = tr.unit
                found = True

    return best_type, best_price, found

# ==== 各ストアごとのルール定義 ====
rules_a = [
    PricingRule(["general"], ["mon", "tue", "wed", "thu", "fri"], [
        TimeRange("11:00", "20:00", "free_time", price_total=1500),
        TimeRange("07:00", "18:00", "per_30_min", price_per_hour=319),
    ]),
    PricingRule(["student", "member"], ["sat", "sun"], [
        TimeRange("07:00", "18:00", "per_30_min", price_per_hour=373),
        TimeRange("11:00", "20:00", "free_time", price_total=2300),
    ]),
]

rules_b = [
    PricingRule(["general"], ["mon", "tue", "wed", "thu", "fri"], [
        TimeRange("11:00", "20:00", "free_time", price_total=1200),
        TimeRange("07:00", "18:00", "per_30_min", price_per_hour=250),
    ]),
    PricingRule(["general"], ["sat", "sun"], [
        TimeRange("07:00", "18:00", "per_30_min", price_per_hour=300),
        TimeRange("11:00", "20:00", "free_time", price_total=2000),
    ]),
]

rules_c = [
    PricingRule(["general"], ["mon", "tue", "wed", "thu", "fri"], [
        TimeRange("11:00", "20:00", "free_time", price_total=1800),
        TimeRange("07:00", "18:00", "per_30_min", price_per_hour=350),
    ]),
    PricingRule(["general"], ["sat", "sun"], [
        TimeRange("07:00", "18:00", "per_30_min", price_per_hour=400),
        TimeRange("11:00", "20:00", "free_time", price_total=2500),
    ]),
]

# ==== Storeのダミーデータ ====
stores = [
    Store(
        name="カラオケまねきねこ 六本木店",
        lat=35.6595,
        lon=139.7005,
        phone="03-1234-5678",
        open_hour ="00:00-24:00",
        rules=rules_a,
        attribute="カラオケまねきねこ"
    ),
    Store(
        name="カラオケパセラ六本木店",
        lat=35.6618,
        lon=139.7353,
        phone="03-8765-4321",
        open_hour ="00:00-24:00",
        rules=rules_b,
        attribute="カラオケパセラ"
    ),
    Store(
        name="カラオケ館 六本木本店",
        lat=35.7289,
        lon=139.7101,
        phone="03-1111-2222",
        open_hour ="00:00-24:00",
        rules=rules_c,
        attribute="カラオケ館"
    ),
]

# # ==== 実行例 ====
# start_time = datetime.fromisoformat("2025-06-17T10:00:00+16:30")
# stay_minutes = 180
# customer_type = "general"

# plan_type, price, ok = find_cheapest_plan(rules, start_time, customer_type, stay_minutes)

# if ok:
#     print(f"最適プラン: {plan_type}（料金: ¥{round(price)}）")
# else:
#     print("該当するプランが見つかりません")
