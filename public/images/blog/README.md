# ブログサムネイル画像

このフォルダにはブログ記事のサムネイル画像を格納します。

## 画像サイズ

### サムネイル画像
- **推奨サイズ:** 800×533px（3:2のアスペクト比）
- **最小サイズ:** 600×400px
- **レティナ対応:** 1200×800px（高解像度ディスプレイ向け）

### OGP画像（SNSシェア用）
- **推奨サイズ:** 1200×630px
- サムネイルと別に用意するか、同じ画像を使用可能

## ファイル命名規則

記事URLに合わせた命名を推奨：

```
blood-flow.jpg          → blog-blood-flow.html用
dryness.jpg            → blog-dryness.html用
femcare-basic.jpg      → blog-femcare-basic.html用
pelvic-training.jpg    → blog-pelvic-training.html用
dark-spots.jpg         → blog-dark-spots.html用
```

## ファイル形式

- **推奨:** JPG（写真・グラデーション系）
- **代替:** PNG（透明背景が必要な場合）
- **軽量化:** WebP形式も推奨（ただしフォールバック用にJPGも用意）

## 画像の設定方法

HTMLで以下のように設定：

```html
<div class="blog-card-image">
    <img src="images/blog/blood-flow.jpg" alt="記事タイトル">
</div>
```

CSSは既に設定済み（object-fit: cover で自動調整）
