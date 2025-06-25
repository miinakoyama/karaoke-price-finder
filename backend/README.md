# Karaoke Price Finder Backend

本リポジトリはカラオケ店舗の検索・料金プラン比較APIのバックエンドです。

---

## 🧑‍💻 技術スタック

- Python 3.10+
- FastAPI（Web APIフレームワーク）
- SQLModel（DB ORM）
- SQLite（開発用DB）
- uv（依存管理・仮想環境・コマンド実行）
- Docker（本番/開発用コンテナ）
- pytest（テスト）
- ruff（静的解析・フォーマット）

---

## 🚀 for non-backend developers

### Dockerでの起動方法

1. **dockerイメージのビルド**

   ```bash
   docker build -t <任意のイメージ名> .
   ```

2. **dockerコンテナの起動**

   ```bash
   docker run -p 8000:80 <任意のイメージ名>
   ```

- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) でAPIドキュメント（Swagger UI）を確認できます。

---

## 🛠️ for backend developers

FastAPI + SQLModel構成。`app/`配下に主要な実装があります。

### ディレクトリ・ファイル構成（`app/`内主要ファイル）

- `main.py` : FastAPIアプリ本体（APIルーティング・CORS・lifespan管理）
- `db.py` : DBエンジン・セッション依存性・テーブル作成/リセット
- `tables.py` : SQLModelによるDBテーブル/ORMモデル定義
- `schemas.py` : API入出力用のPydanticスキーマ
- `services.py` : 検索や詳細取得などAPIごとの業務ロジック
- `utils.py` : 日付判定・最安プラン計算・距離計算などの共通関数
- `seed.py` : DB初期データ投入用スクリプト
- `seed_data.py` : シード用のカラオケ店舗データ
- `models.py` : シード用のdataclassモデル

---

### 開発環境セットアップ（uv推奨）

依存関係のインストールと仮想環境の作成は [uv](https://github.com/astral-sh/uv) で行うことを推奨します。

```bash
uv sync
```

---

### サーバー起動

```bash
uv run fastapi dev
```

---

### テストの実行

pytestもuv経由で実行できます。

```bash
uv run pytest
```

---

### コードチェック・フォーマット（ruff）

ruffによる静的解析・自動修正・フォーマットもuv経由で実行できます。

```bash
uv run ruff check --fix
uv run ruff format
```
