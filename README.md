# 🎤 カラオケ価格検索アプリ – Karaoke Price Finder

現在地または住所を入力するだけで**最安値のカラオケ店**が一瞬で分かるウェブアプリです。

[![Deploy – Vercel](https://img.shields.io/badge/Vercel-Live-black?logo=vercel)](https://k-price.vercel.app)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🛠️ Tech Stack

- **Next.js 14 (App Router) / React 18**
- **Tailwind CSS**

## 🚀 Quick Start

```bash
git clone https://github.com/miinakoyama/karaoke-price-finder.git
cd frontend
npm install
npm run dev
```

Node.js 18 以上での動作を想定しています。開発用サーバーは `http://localhost:3000` で起動します。

## 🗂️ Directory Structure

- `frontend/app` - アプリケーションのページやルーティング
- `frontend/components` - 再利用可能な UI コンポーネント
- `frontend/public` - 画像などの静的アセット

## 🔗 Reference Links

この UI は [v0.dev](https://v0.dev/chat/projects/iSVK7TA8LcM) のチャットから生成したものをベースにしています。

## 🗝️ Google Maps API キーの設定

Google マップ機能を利用するには、`frontend`ディレクトリ直下に`.env.local`ファイルを作成し、以下のように API キーを記載してください。

```
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=<取得したAPIキー>
```

API キーは[Google Cloud Platform](https://console.cloud.google.com/)で取得できます。
