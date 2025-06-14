import type { MetadataRoute } from "next"

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "カラオケ最安検索",
    short_name: "カラオケ検索",
    description: "近くのカラオケ店の料金を比較して最安値を見つけるアプリ",
    start_url: "/",
    display: "standalone",
    background_color: "#F9FAFB",
    theme_color: "#4F46E5",
    icons: [
      {
        src: "/icon-192x192.png",
        sizes: "192x192",
        type: "image/png",
      },
      {
        src: "/icon-512x512.png",
        sizes: "512x512",
        type: "image/png",
      },
    ],
    categories: ["entertainment", "lifestyle"],
    lang: "ja",
    orientation: "portrait-primary",
  }
}
