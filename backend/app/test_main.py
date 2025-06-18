import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_search_shops_basic():
    """
    通常ユーザーでの検索ケース。
    - 緯度経度が渋谷周辺、60分滞在、一般ユーザーとして検索。
    - 1件以上の店舗が返り、各店舗に店名・1人あたり料金が含まれていることを確認。
    - 料金は0円より大きいこと。
    """
    payload = {
        "latitude": 35.6595,
        "longitude": 139.7005,
        "stay_minutes": 60,
        "is_free_time": False,
        "start_time": "12:00",
        "group_size": 2,
        "is_student": False,
        "radius": 1000
    }
    response = client.post("/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)
    assert len(data["results"]) > 0  # 1件以上ヒットすること
    for shop in data["results"]:
        assert "name" in shop
        assert "price_per_person" in shop
        assert shop["price_per_person"] > 0

def test_search_shops_student():
    """
    学生ユーザーでの検索ケース。
    - 緯度経度が渋谷周辺、120分滞在、学生ユーザーとして検索。
    - 1件以上の店舗が返り、各店舗に店名・1人あたり料金が含まれていることを確認。
    - 料金は0円より大きいこと。
    """
    payload = {
        "latitude": 35.6595,
        "longitude": 139.7005,
        "stay_minutes": 120,
        "is_free_time": False,
        "start_time": "15:00",
        "group_size": 3,
        "is_student": True,
        "radius": 1000
    }
    response = client.post("/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)
    assert len(data["results"]) > 0  # 1件以上ヒットすること
    for shop in data["results"]:
        assert "name" in shop
        assert "price_per_person" in shop
        assert shop["price_per_person"] > 0

def test_search_shops_no_result():
    """
    検索条件に該当する店舗が存在しないケース。
    - 緯度経度が0,0（該当店舗なし）、60分滞在、一般ユーザーとして検索。
    - 結果リストが空であることを許容。
    """
    payload = {
        "latitude": 0.0,
        "longitude": 0.0,
        "stay_minutes": 60,
        "is_free_time": False,
        "start_time": "12:00",
        "group_size": 2,
        "is_student": False,
        "radius": 1000
    }
    response = client.post("/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)
    # ダミーデータなので0件になることも許容
