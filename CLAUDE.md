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
- ドメイン: nureclea.com（未取得）
