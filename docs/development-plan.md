# ポートフォリオサイト開発方針

最終更新: 2026-08-10

## 目的

`design-doc/` の画面案を基に、Sho Ikeda の経歴・実績・文章・記録を発信する、軽量で更新しやすい静的ポートフォリオサイトを構築する。

デザインの核は、自然のピクセルアート、紙のような背景、濃紺のタイポグラフィ、黄〜橙のアクセントである。画面案を一枚の画像として再現するのではなく、内容と装飾を分離し、各ページを拡張可能なコンポーネントとして実装する。

## 技術方針

- Astro の静的サイト生成（SSG）を使う。サーバーやデータベースは初期段階では導入しない。
- GitHub Pages での公開を前提に、ビルド時に全ページを出力する。
- 通常のページは Astro コンポーネントだけで配信し、JavaScript は MapLibre GL JS を使う Memory Map と、そのフィルターや詳細表示など、操作が必要な箇所にだけ用いる。
- 記事・実績・Memory の内容は Content Collections で型定義し、Markdown/MDX とフロントマターで管理する。
- 依存パッケージは、標準機能で実現できない場合にのみ追加する。

## ルート設計

| URL | 役割 |
| --- | --- |
| `/` | ヒーロー、注目実績、現在取り組む分野 |
| `/about/` | 経歴、専門領域、学習年表 |
| `/work/` | 実績一覧とプロジェクト詳細への導線 |
| `/writing/` | 記事一覧 |
| `/writing/[slug]/` | 記事詳細 |
| `/contact/` | メール、GitHub、LinkedIn の連絡先 |
| `/memories/` | 地図、カテゴリフィルター、記録詳細 |

## 実装構成

```text
src/
  layouts/
    SiteLayout.astro
  components/
    SiteHeader.astro
    SiteFooter.astro
    PageTitle.astro
    PixelIcon.astro
    ProjectCard.astro
    ArticleList.astro
    MemoryMap.astro
  content/
    projects/
    writings/
    memories/
  pages/
    index.astro
    about.astro
    work.astro
    writing/index.astro
    writing/[slug].astro
    contact.astro
    memories.astro
  styles/
    tokens.css
    global.css
```

## デザイン実装ルール

- 色、余白、罫線、ブレークポイントは `src/styles/tokens.css` に集約する。
- 見出しとナビにはピクセル／ディスプレイ書体、本文には読みやすい等幅系書体を使う。Webフォントのウェイトは必要最小限にする。
- 共通する上部ナビ、フッター、区切り線、黄〜橙のマーカー、矢印リンクをコンポーネント化する。
- ピクセルアートは装飾アセットとして扱い、コンテンツ画像と混在させない。必要なアセットには `image-rendering: pixelated` を限定適用する。
- 画面幅が狭い場合、横並びの情報は1カラムへ切り替える。Work の交互レイアウトはカード列、Memory Map の詳細パネルは地図の下へ移動する。
- `prefers-reduced-motion` に従い、装飾的なアニメーションは停止または簡略化する。

## コンテンツ設計

- **Projects**: タイトル、概要、役割、使用技術、公開リンク、サムネイル、表示順。
- **Writings**: タイトル、公開日、要約、タグ、本文、OGP 用画像。
- **Memories**: タイトル、日付、本文、カテゴリ、位置情報、地図上の座標、複数画像、関連タグ。
- 各コレクションの必須項目と値の形式は Zod スキーマで検証する。

## ブログ（Writings）の投稿方針

### 目的と扱うテーマ

ブログは、成果物の告知だけでなく、ソフトウェア・AI・法律・学習について考えたことを、将来の自分や読者が参照できる形で残す場所とする。投稿のための投稿にはせず、次のいずれかを読者が持ち帰れる記事だけを公開する。

- 実装・設計で得た再利用可能な判断や手順。
- AI、法律、社会と技術の交差点についての根拠を示した考察。
- 学習過程での仮説、失敗、改善点。

カテゴリは画面案と揃え、`software-design`、`ai-engineering`、`law-technology`、`learning-data`、`engineering-systems` を基本とする。タグは検索・関連表示に使うため、1記事あたり 1〜3 個に絞り、同義語を増やさない。

### 記事の構成

1. 冒頭で「何について」「誰に役立つか」「結論」を短く示す。
2. 背景・前提を説明する。
3. 根拠、実例、設計判断を示す。
4. 制約・例外・未解決点を明記する。
5. 実践できる要点または次に調べることをまとめる。

事実、意見、推測を混同しない。外部の事実・統計・法令・他者のコードを扱う場合は、一次情報を優先して出典リンクを添える。生成AIを補助的に使った場合でも、公開前の事実確認と文責は著者が負う。

### ファイルとメタデータ

記事は `src/content/writings/<slug>.md` に追加する。`slug` は英小文字とハイフンのみを使い、公開後は変更しない。初期スキーマは次を採用する。

```md
---
title: "Why common abstractions can go wrong"
description: "Abstraction choices that make systems harder to change."
publishedAt: 2026-07-25
updatedAt: 2026-07-25 # 更新した場合のみ変更する
category: "software-design"
tags: ["dry", "srp"]
draft: false
ogImage: "/images/writings/common-abstractions.png"
---

本文
```

- `draft: true` の記事は本番の一覧・RSS・サイトマップに出さない。
- `publishedAt` は初回公開日として固定し、改稿時は `updatedAt` だけを更新する。
- `description` は検索結果・OGP 用として、日本語ならおおむね 80〜120 文字、英語なら 120〜160 文字を目安にする。
- 見出しは `h2` から始め、`h1` は記事ページ側でタイトルとして1回だけ出力する。

### 公開前チェック

- タイトル、説明、日付、カテゴリ、タグ、アイキャッチを確認する。
- リンク切れ、コード例の動作、出典、誤字、固有名詞を確認する。
- モバイルでの可読性と、見出し階層・画像の代替テキストを確認する。

## Memory Map への記録追加

記録は `src/content/memories/<yyyy-mm-dd>-<slug>.md` に1件ずつ追加する。地図に表示するため、`latitude` と `longitude` は必須とする。座標は `[longitude, latitude]` の順序で MapLibre に渡されるが、フロントマターでは人が読みやすい `latitude`、`longitude` の別フィールドで管理する。

```md
---
title: "Kamakura Cafe"
date: 2026-05-18
summary: "Rainy afternoon in Kamakura."
categories: ["study", "travel", "reflection"]
latitude: 35.3192
longitude: 139.5508
locationLabel: "Kamakura, Kanagawa, Japan"
elevationMeters: 12
images:
  - src: "/images/memories/kamakura-cafe-window.jpg"
    alt: "雨の鎌倉のカフェから見える海と灯台"
  - src: "/images/memories/kamakura-cafe-notebook.jpg"
    alt: "木のテーブルに置かれたノートとコーヒー"
draft: false
---

雨の鎌倉で過ごした午後についての本文。
```

追加手順は以下のとおり。

1. 公開してよい場所かを確認し、必要なら地点を数百メートル〜数キロメートル程度に丸める。
2. 日付と場所を決め、地図サービスなどで緯度・経度を確認してフロントマターへ入力する。
3. `categories` は `nature`、`study`、`travel`、`reflection` の既存値から1つ以上を選ぶ。新しいカテゴリは、フィルター表示・色・文言も追加する必要があるため、安易に増やさない。
4. 写真を `public/images/memories/` に置き、`images` にパスと具体的な代替テキストを追加する。同じ地点には必要な枚数だけ写真を登録できる。
5. ローカルで地図を開き、マーカー位置、フィルター、詳細パネル、モバイル表示を確認する。
6. `draft: false` にして公開する。非公開の下書きは `draft: true` のまま保持する。

正確な自宅・学校・日常の行動パターンを推測できる座標は公開しない。マーカーが重なる場合は、MapLibre 側でクラスタリングまたは同地点の一覧表示を行う。

## Memory Map の実装判断

Memory Map は MapLibre GL JS を用いた実地図として実装する。記録は Content Collection の緯度・経度から GeoJSON に変換し、MapLibre のマーカー／レイヤーとして描画する。マーカーを選択すると、右側（モバイルでは地図の下）の詳細パネルを更新する。カテゴリフィルターは地図上の対象マーカーと一覧の両方に反映する。

詳細パネルの画像領域は、1地点に紐づく複数写真を横方向に閲覧できるギャラリーにする。各写真は独立した `img` 要素として扱い、CSS の横スクロールと scroll snap を基本に実装する。自動送りは行わず、タッチ操作・横スクロール・キーボードで操作できる前後ボタンを提供する。写真の枚数と現在位置が分かる表示（例: `2 / 5`）を付け、各画像には内容を説明する代替テキストを必須にする。

初期版の地図タイルは、API キーを必要としない OpenFreeMap のスタイルを利用し、MapLibre が表示する帰属情報を維持する。公開用サービスには SLA がないため、安定性・独自配色・アクセス規模の要件が生じた段階で、契約済みのタイル提供元またはセルフホストへ移行する。

- MapLibre GL JS とその CSS は、Memory Map のクライアントコードからだけ読み込む。
- 初期表示は記録の中心地点（日本／関東）に固定し、地図のパン・ズーム操作を提供する。
- 各記録は詳細ページまたはアクセシブルな一覧リンクも持たせ、WebGL が利用できない環境でも内容へ到達できるようにする。
- 位置情報を公開して問題がないことを確認し、私的な場所はおおまかな座標へ丸める。

## 実装フェーズ

1. デザイントークン、グローバルスタイル、共通レイアウト、ヘッダー／フッター、モバイルナビを整備する。
2. トップ、About、Work、Contact をプレースホルダーの静的データで実装する。
3. Content Collections と、記事一覧・記事詳細ページを追加する。
4. `maplibre-gl` を追加し、Memory Map に地図タイル、GeoJSON マーカー、カテゴリ絞り込み、選択状態、複数写真ギャラリーを含む詳細パネルを実装する。
5. 画像最適化、ファビコン、OGP、meta description、404 ページ、GitHub Pages 向け設定を整備する。
6. ビルド、主要画面幅、キーボード操作、スクリーンリーダー向け情報、外部リンクを検証する。

## 完了基準

- `npm run build` が成功する。
- 375px、768px、1440px 以上で横スクロールや情報の欠落がない。
- ナビゲーション、フィルター、外部リンクをキーボードだけで操作できる。
- 画像の代替テキスト、見出し階層、フォーカス表示が適切である。
- コンテンツを追加しても、原則としてレイアウトコンポーネントを編集せずに一覧と詳細ページへ反映できる。

## 未確定事項

- ピクセルアート・ロゴ・アイコンの正式な利用素材とライセンス。
- 実績、記事、Memory の公開内容および外部リンク。
- 日本語対応の要否（初期画面案は英語）。
- 将来の地図タイル提供元（独自配色、SLA、セルフホストの要否）。
