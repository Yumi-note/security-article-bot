#!/usr/bin/env python3
"""
情報処理安全確保支援士向け セキュリティ解説記事 自動生成
Gemini REST API 直接呼び出し版
"""

import urllib.request
import urllib.error
import json
import datetime
import os
import sys

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
    "XXE（XML外部エンティティ）インジェクションの詳細",
    "SSRF（サーバーサイドリクエストフォージェリ）の攻撃と対策",
    "パストラバーサル攻撃とディレクトリリスティングの危険性",
    "DNSポイズニングの仕組みとDNSSECによる防御",
    "ARP spoofingと中間者攻撃（MITM）の詳細",
    "ファイアウォールの種類：パケットフィルタリングからNGFWまで",
    "IDS/IPSの仕組みとシグネチャ型・アノマリ型の違い",
    "VPNプロトコル比較：IPsec・OpenVPN・WireGuard",
    "ゼロトラストネットワークアーキテクチャの設計原則",
    "DDoS攻撃の種類と緩和策：CDN・レートリミット・Anycast",
    "Linuxのパーミッションとアクセス制御（DAC/MAC/RBAC）",
    "コンテナセキュリティ：Dockerの隔離機構と脆弱点",
    "Windowsの認証メカニズム：NTLM・Kerberos・SAMLの違い",
    "サプライチェーン攻撃の手法と対策",
    "ランサムウェアの動作原理と感染経路・復旧手順",
    "フォレンジック調査の基礎：証拠保全とタイムライン分析",
    "不正アクセス禁止法の条文と支援士試験での出題傾向",
    "個人情報保護法改正のポイントとGDPRとの比較",
    "情報セキュリティポリシーの策定とISMS（ISO27001）",
    "インシデントレスポンスの手順：NIST SP 800-61の実践",
    "ペネトレーションテストの手法とOWASP Top 10",
    "クラウドセキュリティの基礎：AWSの責任共有モデル",
    "IoTセキュリティのリスクと対策フレームワーク",
]

PROMPT_TEMPLATE = """あなたは情報処理安全確保支援士（登録セキスペ）の試験対策と実務に精通したセキュリティエンジニアです。

以下のテーマでnote投稿用の解説記事を作成してください。

テーマ：{topic}

【条件】
- 文字数：3500文字程度
- 対象：情報処理安全確保支援士の取得を目指す方
- 構成：はじめに／基本概念／技術的な深堀り／攻撃・脆弱性の観点／対策・ベストプラクティス／📝試験対策ポイント／まとめ
- 専門用語は初出時に英語表記を併記
- RFC番号・NIST文書番号など具体的な規格番号を使う
- 「試験ではここが出る！」という視点を随所に入れる"""


def get_today_topic():
    override = os.environ.get("OVERRIDE_TOPIC", "").strip()
    if override:
        return override
    day_of_year = datetime.date.today().timetuple().tm_yday
    return TOPICS[(day_of_year - 1) % len(TOPICS)]


def generate_article(topic):
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise ValueError("GEMINI_API_KEY が設定されていません")

    print(f"[API] キー形式: {api_key[:10]}...")

    prompt = PROMPT_TEMPLATE.format(topic=topic)

    # REST API直接呼び出し（ライブラリ不要）
    # AQ.形式キーはBearer認証で試す
    endpoints = [
        # パターン1: クエリパラメータ
        {
            "url": f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}",
            "headers": {"Content-Type": "application/json"},
        },
        # パターン2: Bearerトークン
        {
            "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
        },
        # パターン3: X-goog-api-key ヘッダー
        {
            "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
            "headers": {
                "Content-Type": "application/json",
                "X-goog-api-key": api_key,
            },
        },
    ]

    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 4096, "temperature": 0.7}
    }).encode()

    last_error = None
    for i, ep in enumerate(endpoints, 1):
        print(f"[API] 試行 {i}/3: {ep['url'][:60]}...")
        try:
            req = urllib.request.Request(
                ep["url"], data=body, method="POST", headers=ep["headers"]
            )
            with urllib.request.urlopen(req, timeout=60) as res:
                result = json.loads(res.read())
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                print(f"[API] ✅ パターン{i}で成功！")
                return text
        except urllib.error.HTTPError as e:
            err_body = e.read().decode()
            print(f"[API] パターン{i} HTTPエラー {e.code}: {err_body[:100]}")
            last_error = err_body
        except Exception as e:
            print(f"[API] パターン{i} エラー: {e}")
            last_error = str(e)

    raise RuntimeError(f"全パターン失敗。最後のエラー: {last_error}")


def save_article(content, topic):
    today = datetime.date.today().strftime("%Y-%m-%d")
    safe_topic = topic[:20].replace("/", "・").replace(" ", "_")
    filename = f"articles/{today}_{safe_topic}.md"
    os.makedirs("articles", exist_ok=True)
    header = f"---\ndate: {today}\ntopic: {topic}\ngenerated_at: {datetime.datetime.now().isoformat()}\n---\n\n"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(header + content)
    return filename


def save_log(topic, filename, success, error=""):
    os.makedirs("logs", exist_ok=True)
    log = {
        "timestamp": datetime.datetime.now().isoformat(),
        "topic": topic,
        "output_file": filename,
        "success": success,
        "error": error,
    }
    with open("logs/execution_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log, ensure_ascii=False) + "\n")


def main():
    print("=" * 60)
    print("🔐 セキュリティ解説記事 自動生成システム")
    print(f"📅 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    topic = get_today_topic()
    print(f"\n📌 本日のテーマ: {topic}\n")

    try:
        article = generate_article(topic)
        print(f"✅ 生成完了（{len(article)}文字）")
    except Exception as e:
        print(f"[ERROR] {e}")
        save_log(topic, "", False, str(e))
        sys.exit(1)

    filename = save_article(article, topic)
    print(f"💾 保存: {filename}")
    save_log(topic, filename, True)

    print("\n📄 プレビュー（先頭200文字）")
    print(article[:200] + "...")
    print("\n✨ 完了！")


if __name__ == "__main__":
    main()
