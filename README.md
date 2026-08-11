# Sho Ikeda Portfolio

Astro で作成したポートフォリオサイトです。英語を既定表示とし、日本語版は `/ja/` 以下で提供します。

## 開発

```sh
npm install
npm run dev
npm run build
npm run preview
```

GitHub Actions は Node.js 24 を使用します。

- `npm run dev` — ローカル開発サーバーを起動
- `npm run build` — `dist/` に静的サイトを出力
- `npm run preview` — ビルド済みサイトをローカルで確認

## 主な構成

```text
src/
├── content/
│   ├── writings/       # 英語記事（Markdown）
│   │   └── ja/         # 日本語記事（Markdown）
│   └── memories/       # 英語 Memory（Markdown）
│       └── ja/         # 日本語 Memory（Markdown）
├── pages/              # 英語ページ
├── pages/ja/           # 日本語ページ
├── components/
└── styles/global.css
public/images/
├── profile.png         # プロフィール画像
├── memories/           # Memory 用の写真
└── projects/           # Project 用の写真
```

## Writing（記事）の追加方法

`src/content/writings/` に、英小文字・ハイフン区切りのファイル名で Markdown を追加します。ファイル名が URL の末尾になります。

例: `src/content/writings/designing-data-contracts.md`

```md
---
title: "Designing Data Contracts"
locale: en
description: "A short summary shown in article lists and metadata."
publishedAt: 2026-08-11
updatedAt: 2026-08-12 # 任意
category: "engineering-systems"
tags: ["data", "architecture"]
draft: false
ogImage: "/images/writings/data-contracts.jpg" # 任意
---

Article body in Markdown.

## A section heading

More content here.
```

利用できる `category` は次の 5 つです。

- `software-design`
- `ai-engineering`
- `law-technology`
- `learning-data`
- `engineering-systems`

`tags` は 1〜3 個、`draft: true` の記事は公開一覧から除外されます。記事は `/writing/<ファイル名>/` に生成されます。

## Memory（地図上の思い出）の追加方法

1. 写真を `public/images/memories/` に配置します。
2. `src/content/memories/` に Markdown を追加します。
3. 緯度・経度を指定します。地図上の写真マーカーはこの座標に表示されます。

例: `src/content/memories/2026-08-11-yokohama-walk.md`

```md
---
title: "Yokohama Walk"
locale: en
date: 2026-08-11
summary: "A short description for the map popup and memory list."
categories: ["travel", "reflection"]
latitude: 35.4437
longitude: 139.6380
locationLabel: "Yokohama, Kanagawa, Japan"
elevationMeters: 8 # 任意
images:
  - src: "/images/memories/yokohama-walk.jpg"
    alt: "A descriptive alt text for the photo"
draft: false
---

The longer memory text goes here.
```

利用できる `categories` は `nature`、`study`、`travel`、`reflection` です。複数指定できます。`images` の先頭の画像が地図マーカーに使われ、残りは詳細ページのギャラリーに使えます。画像がない場合はサイトの既定画像がマーカーに表示されます。

## 日本語版と翻訳

英語・日本語はそれぞれ個別の Markdown として管理します。英語版は `src/content/writings/<slug>.md`（または `memories/<slug>.md`）、日本語版は `src/content/writings/ja/<slug>.md`（または `memories/ja/<slug>.md`）に置き、同じ `<slug>` を使って対応付けます。すべての frontmatter に `locale: en` または `locale: ja` が必要です。

`.github/workflows/create-translations.yml` は、`main` に追加された Writing / Memory Markdown を検出します。反対言語の同名ファイルがまだない場合、Gemini API で翻訳版を作成し、レビュー用 PR を自動作成します。`GEMINI_API_KEY` が未登録の場合は失敗せず、翻訳をスキップします。

GitHub リポジトリの **Settings → Secrets and variables → Actions** で、次の Secret を登録してください。

```text
GEMINI_API_KEY
```

ローカルで翻訳生成を実行する場合は、環境変数を設定してから対象ファイルを渡します。

```sh
GEMINI_API_KEY="..." npm run translate:content -- src/content/writings/new-note.md
```

生成された翻訳は公開前に必ずレビューしてください。固有名詞、技術用語、地名、画像の alt テキストは特に確認が必要です。

Actions タブから **Create translated content** を手動実行することもできます。`en-to-ja` または `ja-to-en` を選ぶと、選んだ翻訳元の最終更新が翻訳先より新しい Markdown と、翻訳先が存在しない Markdown だけを検出して更新します。手動実行では既存の翻訳 Markdown を翻訳結果で更新し、レビュー用 PR を作成します。

既存記事を強制再翻訳したい場合は、Actions の **Run workflow** で次を選びます。

1. `direction`: 翻訳元の言語（例: `en-to-ja`）
2. `mode`: `force`
3. `files`: 翻訳元 Markdown のパス。複数の場合は改行またはカンマで区切る

例:

```text
src/content/writings/common-abstractions.md
src/content/writings/software-engineering-ai-era.md
```

強制モードは更新日時を比較せず、指定した翻訳先 Markdown を Gemini の結果で更新します。作成された PR で必ず内容を確認してからマージしてください。

## 地図について

Memory Map は MapLibre と OpenStreetMap のラスタタイルを使用します。ベースマップの表示にはネットワーク接続が必要です。一方、写真マーカーはサイト内の画像を用い、緯度・経度から表示位置を計算します。

## GitHub Pages への公開

`.github/workflows/deploy-pages.yml` により、`main` への push ごとにサイトをビルドして GitHub Pages へ公開します。リポジトリ作成後に GitHub の **Settings → Pages → Source** で **GitHub Actions** を選択してください。

このリポジトリ名を `SHONOSUKE100.github.io` として作成する場合、公開 URL は `https://shonosuke100.github.io` です。別のリポジトリ名で公開する場合は、`astro.config.mjs` の `base` 設定も必要になります。

## 公開前チェック

変更後は次を実行してください。

```sh
npm run build
```

ビルドが成功すること、英語・日本語の各ページ、記事 URL、Memory Map 上の座標と写真を確認してから公開します。
