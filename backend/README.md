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
