import urllib.request, urllib.error, json, os

api_key = os.environ.get("OPENROUTER_API_KEY", "")

# 試すモデルリスト（無料候補）
models = [
    "meta-llama/llama-3.1-8b-instruct",
    "mistralai/mistral-7b-instruct:free",
    "google/gemma-2-9b-it:free",
    "nousresearch/hermes-3-llama-3.1-405b:free",
]

url = "https://openrouter.ai/api/v1/chat/completions"

for model in models:
    print(f"\n--- テスト: {model} ---")
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "Hi, say hello in Japanese in one sentence"}],
        "max_tokens": 50,
    }).encode()

    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://github.com/Yumi-note/security-article-bot",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            result = json.loads(res.read())
            print(f"SUCCESS: {result['choices'][0]['message']['content']}")
            break  # 成功したら終了
    except urllib.error.HTTPError as e:
        print(f"HTTP_{e.code}: {e.read().decode()[:200]}")
    except Exception as e:
        print(f"ERROR: {e}")
