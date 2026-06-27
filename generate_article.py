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
以下のテーマでnote投稿用の解説記事を2500文字程度で作成してください。

テーマ：{topic}

構成：
# タイトル
## はじめに
## 基本概念
## 技術的な深堀り
## 攻撃・脆弱性の観点
## 対策・ベストプラクティス
## 📝 試験対策ポイント
## まとめ

条件：専門用語は英語表記を併記、RFC/NIST規格番号を使用、試験頻出ポイントを明示"""


def get_topic():
    override = os.environ.get("OVERRIDE_TOPIC", "").strip()
    if override:
        return override
    day = datetime.date.today().timetuple().tm_yday
    return TOPICS[(day - 1) % len(TOPICS)]


def call_gemini(api_key, prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 4096, "temperature": 0.7}
    }).encode("utf-8")

    # X-goog-api-key ヘッダー方式（curlと同じ）
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-goog-api-key": api_key,
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as res:
            result = json.loads(res.read().decode("utf-8"))
            return result["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8")
        print(f"[HTTP ERROR {e.code}]: {err[:300]}")
        raise
    except Exception as e:
        print(f"[ERROR]: {e}")
        raise


def main():
    print("=" * 50)
    print("🔐 セキュリティ記事 自動生成")
    print(f"📅 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        print("[ERROR] GEMINI_API_KEY が未設定")
        sys.exit(1)

    print(f"[INFO] APIキー先頭: {api_key[:10]}... (長さ:{len(api_key)})")

    topic = get_topic()
    print(f"[INFO] テーマ: {topic}")

    prompt = PROMPT.format(topic=topic)

    print("[API] Gemini API呼び出し中...")
    try:
        article = call_gemini(api_key, prompt)
    except Exception as e:
        print(f"[FATAL] 記事生成失敗: {e}")
        sys.exit(1)

    print(f"[OK] {len(article)}文字生成")

    today = datetime.date.today().strftime("%Y-%m-%d")
    safe = topic[:15].replace("/", "・").replace(" ", "_")
    os.makedirs("articles", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    fname = f"articles/{today}_{safe}.md"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"---\ndate: {today}\ntopic: {topic}\n---\n\n" + article)

    log = {"timestamp": datetime.datetime.now().isoformat(), "topic": topic, "file": fname, "chars": len(article)}
    with open("logs/execution_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log, ensure_ascii=False) + "\n")

    print(f"[SAVED] {fname}")
    print("\n📄 プレビュー:")
    print(article[:300] + "...")
    print("\n✨ 完了！")


if __name__ == "__main__":
    main()
