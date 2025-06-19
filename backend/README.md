# 起動
以下backend/ディレクトリで作業するものとする。

## dockerイメージのビルド
```bash
docker build -t backend .
```

## dockerコンテナを動かす
```bash
docker run -p 8000:80 fastapi-app
```
http://127.0.0.1:8000/docs でAPIのドキュメントを確認できる。

# 開発環境セットアップ（uv推奨）

依存関係のインストールと仮想環境の作成はuvで行うことを推奨します。

```bash
uv sync
```

## テストの実行

pytestもuv経由で実行できます。

```bash
uv run pytest
```

## コードチェック・フォーマット（ruff）

ruffによる静的解析・自動修正・フォーマットもuv経由で実行できます。

```bash
uv run ruff check --fix
uv run ruff format
```
