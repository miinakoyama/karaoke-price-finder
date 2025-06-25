# from fastapi.testclient import TestClient

# from app.main import app

# client = TestClient(app)


# def test_search_shops_basic():
#     """
#     通常ユーザーでの検索ケース。
#     - 緯度経度が渋谷周辺、60分滞在、一般ユーザーとして検索。
#     - 1件以上の店舗が返り、各店舗に店名・1人あたり料金が含まれていることを確認。
#     - 料金は0円より大きいこと。
#     """
#     payload = {
#         "latitude": 35.6595,
#         "longitude": 139.7005,
#         "stay_minutes": 60,
#         "start_time": "12:00",
#         "group_size": 2,
#         "is_student": False,
#         "radius": 1000,
#     }
#     response = client.post("/search", json=payload)
#     assert response.status_code == 200
#     data = response.json()
#     assert "results" in data
#     assert isinstance(data["results"], list)
#     assert len(data["results"]) > 0
#     for shop in data["results"]:
#         assert "name" in shop
#         assert "price_per_person" in shop
#         assert shop["price_per_person"] > 0
#         assert "icon_url" in shop
#         assert "all_plans" in shop
#         assert "latitude" in shop
#         assert "longitude" in shop
#         assert "phone" in shop
#         assert "distance" in shop  # 直線距離が含まれることを確認
#         # drink_typeは除外


# def test_search_shops_student():
#     """
#     学生ユーザーでの検索ケース。
#     - 緯度経度が渋谷周辺、120分滞在、学生ユーザーとして検索。
#     - 1件以上の店舗が返り、各店舗に店名・1人あたり料金が含まれていることを確認。
#     - 料金は0円より大きいこと。
#     """
#     payload = {
#         "latitude": 35.6595,
#         "longitude": 139.7005,
#         "stay_minutes": 120,
#         "start_time": "15:00",
#         "group_size": 3,
#         "is_student": True,
#         "radius": 1000,
#     }
#     response = client.post("/search", json=payload)
#     assert response.status_code == 200
#     data = response.json()
#     assert "results" in data
#     assert isinstance(data["results"], list)
#     assert len(data["results"]) > 0
#     for shop in data["results"]:
#         assert "name" in shop
#         assert "price_per_person" in shop
#         assert shop["price_per_person"] > 0
#         assert "icon_url" in shop
#         assert "all_plans" in shop
#         assert "latitude" in shop
#         assert "longitude" in shop
#         assert "phone" in shop
#         assert "distance" in shop  # 直線距離が含まれることを確認
#         # drink_typeは除外


# def test_search_shops_no_result():
#     """
#     検索条件に該当する店舗が存在しないケース。
#     - 緯度経度が0,0（該当店舗なし）、60分滞在、一般ユーザーとして検索。
#     - 結果リストが空であることを許容。
#     """
#     payload = {
#         "latitude": 0.0,
#         "longitude": 0.0,
#         "stay_minutes": 60,
#         "start_time": "12:00",
#         "group_size": 2,
#         "is_student": False,
#         "radius": 1000,
#     }
#     response = client.post("/search", json=payload)
#     assert response.status_code == 200
#     data = response.json()
#     assert "results" in data
#     assert isinstance(data["results"], list)
#     # ダミーデータなので0件になることも許容


# def test_get_shop_detail_basic():
#     """
#     店舗詳細取得APIの基本動作テスト。
#     - 店舗ID=1, 開始時刻12:00, 60分, 一般ユーザー
#     - プランリストが1件以上返ること
#     - 各プランにunit, price, start, end, customer_typeが含まれる
#     """
#     payload = {"shop_id": "1", "start_time": "12:00", "stay_minutes": 60, "is_student": False}
#     response = client.post("/get_detail", json=payload)
#     assert response.status_code == 200
#     data = response.json()
#     assert "shop_id" in data
#     assert "name" in data
#     assert "plans" in data
#     assert isinstance(data["plans"], list)
#     assert len(data["plans"]) > 0
#     for plan in data["plans"]:
#         assert "unit" in plan
#         assert "price" in plan
#         assert "start" in plan
#         assert "end" in plan
#         assert "customer_type" in plan
