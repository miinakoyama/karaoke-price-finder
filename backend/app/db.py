from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

# SQLiteファイル名と接続URL
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}

# SQLModel用のDBエンジン作成
engine = create_engine(sqlite_url, connect_args=connect_args)


# FastAPI依存性として使うDBセッション生成関数
def get_session():
    """
    SQLModelのSessionを生成し、with文で自動クローズする。
    FastAPIのDependsで利用。
    """
    with Session(engine) as session:
        yield session

# FastAPI依存性注入用の型エイリアス
SessionDep = Annotated[Session, Depends(get_session)]


# テーブル作成関数
def create_db_and_tables():
    """
    DBに全テーブルを新規作成する（既存テーブルはそのまま）。
    """
    SQLModel.metadata.create_all(engine)

# テーブルリセット関数
def reset_db_and_tables():
    """
    DBの全テーブルを一度削除し、再作成する（初期化用）。
    """
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
