#!/usr/bin/env python3
"""
情報処理安全確保支援士向け セキュリティ解説記事 自動生成スクリプト
毎朝8時にGitHub Actionsから実行される（Gemini API使用・無料）
"""

import google.genai as genai
import datetime
import os
import json
import sys

# ==========================================
# テーマリスト（35日分・自動循環）
# ==========================================
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

SYSTEM_PROMPT = """あなたは情報処理安全確保支援士（登録セキスペ）の試験対策と実務に精通した
セキュリティエンジニアです。

以下の条件で記事を作成してください：

【対象読者】
- 情報処理安全確保支援士の取得を目指している方
- ITエンジニア・セキュリティ担当者

【記事の条件】
- 文字数：2500文字程度（±200文字）
- note投稿を想定した読みやすい文体
- 技術的に正確で深い内容
- 試験に出るポイントを明示する
- 実務での応用も含める

【構成】
1. タイトル（#）
2. はじめに（200文字程度）
3. 基本概念（##）
4. 技術的な深堀り（##）
5. 攻撃・脆弱性の観点（##）
6. 対策・ベストプラクティス（##）
7. 📝 試験対策ポイント（##）
8. まとめ（##）

【ルール】
- 専門用語には初出時に英語表記を添える
- RFC番号・NIST文書番号など具体的な規格番号を使う
- 「試験ではここが出る！」という視点を随所に入れる"""


def get_today_topic() -> str:
    override = os.environ.get("OVERRIDE_TOPIC", "").strip()
    if override:
        return override
    day_of_year = datetime.date.today().timetuple().tm_yday
    return TOPICS[(day_of_year - 1) % len(TOPICS)]


def generate_article(topic: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY が設定されていません")

    client = genai.Client(api_key=api_key)

    prompt = f"{SYSTEM_PROMPT}\n\n以下のテーマで記事を作成してください：\n\n{topic}"

    print(f"[API] Gemini APIに記事生成をリクエスト中...")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text


def save_article(content: str, topic: str) -> str:
    today = datetime.date.today().strftime("%Y-%m-%d")
    safe_topic = topic[:20].replace("/", "・").replace(" ", "_")
    filename = f"articles/{today}_{safe_topic}.md"
    os.makedirs("articles", exist_ok=True)

    header = f"---\ndate: {today}\ntopic: {topic}\ngenerated_at: {datetime.datetime.now().isoformat()}\n---\n\n"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(header + content)
    return filename


def save_log(topic: str, filename: str, success: bool, error: str = ""):
    os.makedirs("logs", exist_ok=True)
    log = {
        "timestamp": datetime.datetime.now().isoformat(),
        "date": datetime.date.today().isoformat(),
        "topic": topic,
        "output_file": filename,
        "success": success,
        "error": error,
    }
    with open("logs/execution_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log, ensure_ascii=False) + "\n")


def main():
    print("=" * 60)
    print("🔐 セキュリティ解説記事 自動生成システム（Gemini版）")
    print(f"📅 実行日時: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    topic = get_today_topic()
    print(f"\n📌 本日のテーマ: {topic}\n")

    try:
        article = generate_article(topic)
        print(f"✅ 記事生成完了（{len(article)}文字）")
    except Exception as e:
        print(f"[ERROR] 記事生成失敗: {e}")
        save_log(topic, "", False, str(e))
        sys.exit(1)

    try:
        filename = save_article(article, topic)
        print(f"💾 ファイル保存: {filename}")
    except Exception as e:
        print(f"[ERROR] ファイル保存失敗: {e}")
        save_log(topic, "", False, str(e))
        sys.exit(1)

    save_log(topic, filename, True)

    print("\n" + "=" * 60)
    print("📄 記事プレビュー（先頭300文字）")
    print("=" * 60)
    print(article[:300] + "...")
    print("\n✨ 完了！")


if __name__ == "__main__":
    main()
