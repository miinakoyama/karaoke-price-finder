"""
ユーティリティ関数の最低限テスト。
- haversine: 距離計算の正常系
"""

from app.utils import haversine


def test_haversine_distance_basic():
    """
    2点間の距離計算が正しいことを検証。
    - 東京駅-大阪駅間で約400km（メートル単位で検証）
    """
    tokyo = (35.681236, 139.767125)
    osaka = (34.702485, 135.495951)
    dist = haversine(tokyo[0], tokyo[1], osaka[0], osaka[1])
    assert 390_000 < dist < 410_000  # メートル単位
