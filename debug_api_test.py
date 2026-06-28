import urllib.request, urllib.error, json, os

api_key = os.environ.get("OPENROUTER_API_KEY", "")

# DeepSeekのモデル候補を試す
models = [
    "deepseek/deepseek-r1:free",
    "deepseek/deepseek-chat:free",
    "deepseek/deepseek-r1-distill-llama-70b:free",
    "deepseek/deepseek-r1-distill-qwen-32b:free",
]

url = "https://openrouter.ai/api/v1/chat/completions"

for model in models:
    print(f"--- {model} ---")
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "日本語でこんにちはと言って"}],
        "max_tokens": 30,
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
            break
    except urllib.error.HTTPError as e:
        print(f"HTTP_{e.code}: {e.read().decode()[:150]}")
    except Exception as e:
        print(f"ERROR: {e}")
