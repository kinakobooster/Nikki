# Nikki プロジェクト仕様書

このドキュメントは、Nikkiプロジェクトの技術仕様と実装詳細を記載しています。

## プロジェクト概要

Nikkiは縦書きレイアウトの日記サイトです。2025年7月20日から8月31日まで、毎日短い文章を公開します。

## 技術スタック

- 静的サイトジェネレーター: Python (generate_site.py)
- フロントエンド: Pure HTML/CSS/JavaScript
- 環境変数管理: python-dotenv (.env)
- アクセスカウンター: Counter API V2
- ホスティング: GitHub Pages

## ディレクトリ構造

```
/
├── README.md           # プロジェクト説明
├── CLAUDE.md          # 技術仕様書（このファイル）
├── generate_site.py   # 静的サイトジェネレーター
├── index.html         # 生成されるHTMLファイル（gitignore済み）
├── .env               # 環境変数設定（Counter API設定）
├── docs/              # マークダウン記事
│   ├── 0000.md       # イントロダクション
│   ├── 20250720.md   # 7月20日の記事
│   └── 20250721.md   # 7月21日の記事
└── .gitignore        # Git除外設定
```

## 縦書きレイアウト仕様

### 基本概念
- **右が頭（始まり）、左がお尻（終わり）**
- 記事は右から左へ配置（最新→最古）
- スクロールは横方向（overflow-x: scroll）

### 記事の配置
```
[最新記事(20250721)] → [20250720] → [0000(最古)]
     右端                                左端
```


## スタイリング

### フォント設定
- 本文：明朝体（'Hiragino Mincho ProN', 'Yu Mincho'）
- 見出し：ゴシック体（'Hiragino Kaku Gothic ProN', 'Yu Gothic'）
- 見出しの太さ：font-weight: 700

### レイアウト
- 縦書き：writing-mode: vertical-rl
- 記事間マージン：60px
- コンテナの高さ：80vh

## 重要な注意事項

### コード構造上の注意点

1. **記事順序の管理**
   - `md_files` は通常の昇順ソート（0000, 20250720, 20250721...）
   - HTMLでは `reversed(md_files)` で右から左配置（最新→最古）
   - contents配列のインデックス：[0]=最新記事, [1]=前の記事, [2]=最古記事

2. **ドットの生成とインデックス**
   - ドット生成：`range(len(md_files) - 1, -1, -1)` で逆順
   - data-index値：2(最新記事), 1(前の記事), 0(最古記事)
   - **重要**：記事数が変わるとdata-index値も変わる

3. **スクロール位置計算の複雑性**
   - `updateActiveDot()`: スクロール進行度を逆算してアクティブドット判定
   - ナビゲーション: 各ドットのdata-indexに対してハードコードされた分岐処理
   - **問題**：記事数が変わると計算ロジックの修正が必要

### 今後の記事追加時の対応

新しい記事（例：20250722.md）を追加する場合：

1. **自動対応される部分**
   - 記事のHTML生成
   - ドットの個数

2. **手動修正が必要な部分**
   - `updateActiveDot()` 関数のactiveIndex計算
   - ドットクリックハンドラーの分岐処理（現在は3記事前提）
   - 各ドットの動作先の再定義

## 環境変数設定

### .envファイルの設定項目

```bash
# Counter API V2 設定
COUNTER_WORKSPACE=nikkisite2025
ACCESS_COUNTER=totalvisits
LIKE_COUNTER=totallikes
```

### 設定項目の説明

- `COUNTER_WORKSPACE`: Counter API V2のワークスペース名
- `ACCESS_COUNTER`: アクセス数用のカウンター名
- `LIKE_COUNTER`: いいね数用のカウンター名

### generate_site.pyでの使用

環境変数は`os.getenv()`を使用してJavaScriptテンプレート内に埋め込まれます。環境変数が設定されていない場合は、デフォルト値が使用されます。

## 更新履歴

- 2025-01-22: Counter API設定を.envファイルに外部化
- 2025-01-22: python-dotenvパッケージの依存関係を追加
- 2025-01-20: ドットナビゲーション仕様を縦書きレイアウトに最適化
- 2025-01-20: 見出しをゴシック体に変更
- 2025-01-20: index.htmlをgitignoreに追加
- 2025-01-20: コード構造の注意事項を追記