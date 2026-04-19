# ヌレクリア ブランドサイト

> **基本ルール**: ~/projects/CLAUDE.md も併せて参照してください

ヌレクリア（フェムケアクリーム）のブランド公式サイト。商品紹介・モニター募集の信頼基盤として機能する。

## 技術スタック

- **フレームワーク**: HTML/CSS（静的サイト）
- **スタイリング**: CSS（フレームワークなし）
- **パッケージマネージャー**: なし

## よく使うコマンド

- `python3 -m http.server 8000` - ローカルプレビュー
- `npx wrangler pages deploy public --project-name nureclea` - 本番デプロイ

## プロジェクト構成

- `src/` - 設計書・ソースファイル
- `tasks/` - タスク管理
- `client-data/` - クライアントデータ置き場

## デプロイ

- ホスティング: Cloudflare Pages
- ドメイン: nureclea.com

## コラム記事の追加ルール

新しいコラム記事を作成するときは **必ず以下の手順に従う**。

### 1. テンプレートを使う
`src/article-template.html` をベースにする。{{変数}} をすべて実際の値に置き換えること。

### 2. articles.json に追記する
`public/articles.json` に以下の形式で追加する（publishDate の昇順を維持）。
```json
{
  "file": "blog-xxx.html",
  "publishDate": "YYYY-MM-DD",
  "category": "フェムケア or 感度アップ",
  "title": "記事タイトル",
  "excerpt": "一覧ページに表示する概要文（60〜80文字）",
  "image": null
}
```

### 3. SEO・LLMO タグの必須要素（テンプレートに含まれているが要確認）
- `<title>` : 記事タイトル＋「｜ヌレクリア」
- `<meta name="description">` : 120〜150文字
- OGP（og:title / og:description / og:url / og:type=article）
- `<link rel="canonical">` : `https://nureclea.com/ファイル名`
- JSON-LD Article スキーマ
- JSON-LD FAQPage スキーマ（FAQ の class 名は必ず `faq-question` / `faq-answer` にする）

### 4. 既存記事にSEOを一括追加するとき
```bash
python3 src/add_seo.py
```
articles.json に登録済みの記事にのみ適用される。og:title が既にある記事はスキップ。
