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
以下のテーマでnote投稿用の解説記事を3500文字程度で日本語で作成してください。

テーマ：{topic}

【読者像】
- ITエンジニア歴1〜3年、セキュリティは初学者〜中級者
- 情報処理安全確保支援士の取得を目指している
- 「なぜそうなるのか」の背景から理解したい人

【必須構成・各セクション文字数目安】

# タイトル

## はじめに（200文字）
- このテーマが現場でなぜ重要か、知らないとどんなリスクがあるか

## 前提知識（500文字）
- 初学者が「そもそも○○って何？」と思う部分を先に解消
- 関連する用語・プロトコル・仕組みを丁寧に説明
- ASCII図で前提の構造を可視化

## 基本概念（600文字）
- テーマの核心となる仕組みをわかりやすく説明
- ASCII図でフロー・構造を図解

## 技術的な深堀り（700文字）
- 具体的なフロー・アルゴリズムを数値・規格番号（RFC・NIST等）を交えて解説
- ASCII図でシーケンス図や詳細フローを表現

## 攻撃・脆弱性の観点（500文字）
- どのように悪用されるか、実際の攻撃フローをASCII図で図解
- 有名な攻撃事例や脆弱性（CVE番号等）

## 対策・ベストプラクティス（500文字）
- 具体的な対策を箇条書きと図で整理
- 実装時の注意点・設定例

## 📝 試験対策ポイント（300文字）
- 支援士試験で頻出のポイントを表形式でまとめ
- 間違えやすいポイント・引っかけ問題パターン

## まとめ（200文字）
- 要点を3〜5行で整理、次に学ぶテーマへの誘導

【図の要件】各セクションに必ずASCII図または表を1つ以上入れる

【その他の条件】
- 専門用語は初出時に英語表記を併記
- RFC番号・NIST SP番号など具体的な規格番号を使用
- ⚠️ 試験ではここが出る！という注釈を要所に入れる
- 難しい概念には具体的なたとえ話を添える"""


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
        "max_tokens": 6000,
    }).encode("utf-8")

    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://github.com/Yumi-note/security-article-bot",
        "X-Title": "Security Article Bot",
    })
    with urllib.request.urlopen(req, timeout=240) as res:
        result = json.loads(res.read().decode("utf-8"))
        return result["choices"][0]["message"]["content"]


def main():
    print("=" * 50)
    print("🔐 セキュリティ記事 自動生成（DeepSeek R1・3500文字版）")
    print(f"📅 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        print("[ERROR] OPENROUTER_API_KEY が未設定")
        sys.exit(1)

    print(f"[INFO] モデル: deepseek/deepseek-r1")
    topic = get_topic()
    print(f"[INFO] テーマ: {topic}")

    try:
        print("[API] DeepSeek R1 呼び出し中...")
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
    print("\n📄 プレビュー（先頭400文字）:")
    print(article[:400] + "...")
    print("\n✨ 完了！")


if __name__ == "__main__":
    main()
