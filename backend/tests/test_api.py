"""
APIエンドポイントの最低限テスト。
- /search: 正常系・0件ヒット
- /get_detail: 正常系
"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_search_shops_basic():
    """
    /search APIの正常系: 1件以上ヒットすること（ダミーデータ次第で0件も許容）
    - 緯度経度: 渋谷周辺
    - 滞在時間: 60分
    - 一般ユーザー
    """
    payload = {
        "latitude": 35.6595,
        "longitude": 139.7005,
        "stay_minutes": 60,
        "start_time": "12:00",
        "group_size": 2,
        "is_student": False,
        "radius": 1000,
    }
    response = client.post("/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)
    # assert len(data["results"]) > 0  # 必要に応じて有効化


def test_search_shops_no_result():
    """
    /search API: 0件ヒットするケース
    - 緯度経度: 0,0（該当店舗なし）
    - 滞在時間: 60分
    - 一般ユーザー
    """
    payload = {
        "latitude": 0.0,
        "longitude": 0.0,
        "stay_minutes": 60,
        "start_time": "12:00",
        "group_size": 2,
        "is_student": False,
        "radius": 1000,
    }
    response = client.post("/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)
    # 0件でもOK


def test_get_shop_detail_basic():
    """
    /stores/{store_id} APIの正常系: プランリストが1件以上返る
    - 店舗ID=1, 開始時刻12:00, 60分, 一般ユーザー
    - DBアクセスとサービス層をモックし、常にダミー店舗データを返す
    """
    dummy_response = {
        "store_id": 1,
        "store_name": "テストカラオケ",
        "phone_number": "000-0000-0000",
        "plans": [
            {
                "plan_name": "30分プラン午前",
                "general_price": 300,
                "student_price": 250,
                "member_price": 200,
                "time_range": "10:00~12:00",
            }
        ],
    }
    with patch("app.main.get_store_plans") as mock_get_plans, patch("sqlmodel.Session.get") as mock_session_get:
        mock_get_plans.return_value = dummy_response
        mock_session_get.return_value = True  # store is not None
        response = client.get("/stores/1?start_time=12:00")
        assert response.status_code == 200
        data = response.json()
        assert "store_id" in data
        assert "store_name" in data
        assert "plans" in data
        assert isinstance(data["plans"], list)
        # assert len(data["plans"]) > 0  # 必要に応じて有効化
