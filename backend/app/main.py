from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .db import (
    SessionDep,
    reset_db_and_tables,
)
from .schemas import SearchRequest, SearchResponse, StoreDetailResponse
from .seed import seed_karaoke_stores
from .services import get_store_plans, search_karaoke_shops
from .tables import (
    KaraokeStoreDB,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # アプリ起動時にDBをリセットし、初期データをシード
    reset_db_and_tables()
    seed_karaoke_stores()
    yield  # アプリのライフサイクルを管理


app = FastAPI(lifespan=lifespan)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React側のURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/stores/{store_id}", response_model=StoreDetailResponse)
async def get_store_detail(
    store_id: int,
    session: SessionDep,
    start_time: Annotated[str, Query(description="開始時刻（例: '23:00'）")],
):
    """
    指定した店舗ID・利用開始時刻から、その日の営業終了時刻までに一部でも重なる全プラン詳細を返すエンドポイント。
    - 日付をまたぐ営業時間（例: 10:00〜翌5:00）にも対応。
    - 例1: 6/23(月) AM2:00に検索 → 6/23 2:00〜5:00までに利用可能なプランを全て返す
    - 例2: 6/22(日) 16:00に検索 → 6/22 16:00〜6/23 5:00までに利用可能なプランを全て返す
    - プランの時間帯が検索区間（start_time〜営業終了時刻）と一部でも重なっていれば返す
    """
    store = session.get(KaraokeStoreDB, store_id)
    if store is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return get_store_plans(store, start_time)


@app.post("/search", response_model=SearchResponse)
async def search_shops(request: SearchRequest, session: SessionDep):
    """
    検索条件に合致するカラオケ店舗のリストを返すエンドポイント。
    - 並び順は店舗の最安値順。
    - 距離・会員区分・学生区分・滞在時間など複数条件で絞り込み可能。
    - ドリンクオプションや料金内訳も返す。
    """
    return search_karaoke_shops(request, session)


@app.get("/hello")
async def hello():
    """
    ヘルスチェック用エンドポイント。
    サーバーが正常に稼働しているか確認するためのシンプルなAPI。
    """
    return {"message": "Hello!"}
