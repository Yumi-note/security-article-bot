# 🔐 セキュリティ解説記事 自動生成Bot

情報処理安全確保支援士の取得を目指す方向けに、毎朝8時（JST）にセキュリティ解説記事を自動生成してGitHubにコミットします。

## 仕組み

```
毎朝8:00 JST
    ↓
GitHub Actions 起動（Ubuntu サーバー上）
    ↓
Python スクリプト実行
    ↓
Claude API（claude-opus-4-6）で2500文字の記事生成
    ↓
articles/ フォルダにMarkdownで保存
    ↓
GitHubに自動コミット
    ↓
あなたがコピーしてnoteに投稿
```

## セットアップ手順

### 1. このリポジトリをFork or Clone

```bash
git clone https://github.com/あなたのユーザー名/security-article-bot.git
cd security-article-bot
```

### 2. Claude APIキーを取得

1. https://console.anthropic.com にアクセス
2. 「API Keys」→「Create Key」
3. キーをコピー（`sk-ant-...`で始まる文字列）

### 3. GitHub SecretsにAPIキーを登録

1. リポジトリの「Settings」→「Secrets and variables」→「Actions」
2. 「New repository secret」をクリック
3. Name: `ANTHROPIC_API_KEY`
4. Value: コピーしたAPIキーを貼り付け
5. 「Add secret」をクリック

### 4. GitHub Actionsを有効化

リポジトリの「Actions」タブ → 「I understand my workflows, go ahead and enable them」

### 5. 動作確認（手動実行）

1. 「Actions」タブ → 「毎朝セキュリティ記事生成」
2. 「Run workflow」→ 「Run workflow」ボタン
3. 数分後に `articles/` フォルダに記事が生成される

## ローカルでのテスト

```bash
# 依存パッケージのインストール
pip install anthropic

# APIキーを環境変数に設定
export ANTHROPIC_API_KEY="sk-ant-xxxxxx"

# 実行
python generate_article.py

# テーマを指定して実行
OVERRIDE_TOPIC="SQLインジェクションの詳細" python generate_article.py
```

## ファイル構成

```
security-article-bot/
├── .github/
│   └── workflows/
│       └── daily_article.yml    # GitHub Actionsの設定
├── articles/                     # 生成された記事（自動作成）
│   └── 2024-01-15_PKIと電子証明書.md
├── logs/                         # 実行ログ（自動作成）
│   └── execution_log.jsonl
├── generate_article.py           # メインスクリプト
├── requirements.txt
└── README.md
```

## 記事テーマ一覧（35種類・自動循環）

- PKIと電子証明書
- TLS1.3ハンドシェイク
- SQLインジェクション
- バッファオーバーフロー
- XSS・CSRF・XXE・SSRF
- ゼロトラストネットワーク
- ランサムウェア
- 不正アクセス禁止法
- ...など35テーマ

## noteへの投稿方法

1. `articles/` フォルダから当日の`.md`ファイルを開く
2. 内容をコピー
3. noteの投稿画面に貼り付け（Markdownは自動変換される）
4. 公開！

## コスト目安

Claude API（claude-opus-4-6）で1記事あたり約2500文字生成時：
- 入力トークン：約500〜800
- 出力トークン：約1500〜2000
- **1記事あたり約2〜4円**（月60〜120円程度）
