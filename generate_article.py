#!/usr/bin/env python3
import urllib.request, urllib.error
import json, datetime, os, sys

TOPICS = [
    "PKIと電子証明書：信頼の連鎖とX.509の仕組み",
    "TLS1.3ハンドシェイクの詳細フローと前方秘匿性",
    "ハッシュ関数の仕組みとSHA-256の安全性",
    "デジタル署名の原理とRSA・ECDSAの違い",
    "OAuth2.0とOpenID Connectの認証フロー徹底解説",
    "多要素認証（MFA）の種類と実装上の注意点",
    "パスワードハッシュ化：bcrypt・scrypt・Argon2の比較",
    "JWTの構造と安全な実装のポイント",
    "SQLインジェクションの仕組みと完全な対策",
    "バッファオーバーフロー攻撃の原理とメモリ保護機構",
    "XSS（クロスサイトスクリプティング）の種類と対策",
    "CSRF攻撃の仕組みとSameSite Cookieによる防御",
    "DNSポイズニングの仕組みとDNSSECによる防御",
    "ファイアウォールの種類：パケットフィルタリングからNGFWまで",
    "IDS/IPSの仕組みとシグネチャ型・アノマリ型の違い",
    "VPNプロトコル比較：IPsec・OpenVPN・WireGuard",
    "ゼロトラストネットワークアーキテクチャの設計原則",
    "DDoS攻撃の種類と緩和策：CDN・レートリミット・Anycast",
    "Linuxのパーミッションとアクセス制御（DAC/MAC/RBAC）",
    "コンテナセキュリティ：Dockerの隔離機構と脆弱点",
    "Windowsの認証：NTLM・Kerberos・SAMLの違い",
    "サプライチェーン攻撃の手法と対策",
    "ランサムウェアの動作原理と感染経路・復旧手順",
    "フォレンジック調査の基礎：証拠保全とタイムライン分析",
    "不正アクセス禁止法と支援士試験での出題傾向",
    "個人情報保護法改正のポイントとGDPRとの比較",
    "情報セキュリティポリシーの策定とISMS（ISO27001）",
    "インシデントレスポンスの手順：NIST SP 800-61の実践",
    "ペネトレーションテストの手法とOWASP Top 10",
    "クラウドセキュリティの基礎：AWSの責任共有モデル",
    "IoTセキュリティのリスクと対策フレームワーク",
    "XXE（XML外部エンティティ）インジェクションの詳細",
    "SSRF（サーバーサイドリクエストフォージェリ）の攻撃と対策",
    "ARP spoofingと中間者攻撃（MITM）の詳細",
    "パストラバーサル攻撃とディレクトリリスティングの危険性",
]

PROMPT = """あなたは情報処理安全確保支援士の試験対策に精通したセキュリティエンジニアです。
以下のテーマでnote投稿用の解説記事を2500文字程度で日本語で作成してください。

テーマ：{topic}

【重要】以下のASCII図を必ず各セクションに1つ以上含めてください：
- フロー図（処理の流れを矢印で表現）
- 構成図（コンポーネントの関係を箱と矢印で表現）
- 比較表（項目を縦横で整理）

ASCII図の例：
```
┌─────────┐     ┌─────────┐
│クライアント│────→│ サーバー │
└─────────┘     └─────────┘
```

```
攻撃者          Webサーバー      DBサーバー
  │                │                │
  │── 悪意のSQL ──→│                │
  │                │── クエリ実行 ──→│
  │                │←── 全データ ───│
  │←── 情報漏洩 ───│                │
```

構成：
# タイトル
## はじめに（このテーマが重要な理由）
## 基本概念（ASCII図で仕組みを図解）
## 技術的な深堀り（フロー図・詳細な説明）
## 攻撃・脆弱性の観点（攻撃フロー図）
## 対策・ベストプラクティス（対策の構成図）
## 📝 試験対策ポイント（表形式でまとめ）
## まとめ

条件：
- 専門用語は英語表記を併記
- RFC/NIST規格番号を使用
- 試験頻出ポイントを明示
- 各セクションに必ずASCII図か表を入れる"""


def get_topic():
    override = os.environ.get("OVERRIDE_TOPIC", "").strip()
    if override:
        return override
    day = datetime.date.today().timetuple().tm_yday
    return TOPICS[(day - 1) % len(TOPICS)]


def call_api(api_key, prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    body = json.dumps({
        "model": "deepseek/deepseek-r1",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4096,
    }).encode("utf-8")

    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://github.com/Yumi-note/security-article-bot",
        "X-Title": "Security Article Bot",
    })
    with urllib.request.urlopen(req, timeout=180) as res:
        result = json.loads(res.read().decode("utf-8"))
        return result["choices"][0]["message"]["content"]


def main():
    print("=" * 50)
    print("🔐 セキュリティ記事 自動生成（DeepSeek版）")
    print(f"📅 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        print("[ERROR] OPENROUTER_API_KEY が未設定")
        sys.exit(1)

    print(f"[INFO] モデル: deepseek/deepseek-r1:free")
    topic = get_topic()
    print(f"[INFO] テーマ: {topic}")

    try:
        print("[API] DeepSeek呼び出し中（少し時間がかかります）...")
        article = call_api(api_key, PROMPT.format(topic=topic))
    except Exception as e:
        print(f"[FATAL] {e}")
        sys.exit(1)

    print(f"[OK] {len(article)}文字生成")

    today = datetime.date.today().strftime("%Y-%m-%d")
    safe = topic[:15].replace("/", "・").replace(" ", "_")
    os.makedirs("articles", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    fname = f"articles/{today}_{safe}.md"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"---\ndate: {today}\ntopic: {topic}\nmodel: deepseek-r1\n---\n\n" + article)

    log = {"timestamp": datetime.datetime.now().isoformat(), "topic": topic, "file": fname, "chars": len(article), "model": "deepseek-r1"}
    with open("logs/execution_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log, ensure_ascii=False) + "\n")

    print(f"[SAVED] {fname}")
    print("\n📄 プレビュー（先頭300文字）:")
    print(article[:300] + "...")
    print("\n✨ 完了！")


if __name__ == "__main__":
    main()
