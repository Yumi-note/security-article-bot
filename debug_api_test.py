import urllib.request, urllib.error, json, os

api_key = os.environ.get("OPENROUTER_API_KEY", "")
print(f"KEY_PREFIX: {api_key[:15]}")

url = "https://openrouter.ai/api/v1/chat/completions"
body = json.dumps({
    "model": "meta-llama/llama-3.1-8b-instruct:free",
    "messages": [{"role": "user", "content": "Hi"}],
    "max_tokens": 10,
}).encode()

req = urllib.request.Request(url, data=body, method="POST", headers={
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
    "HTTP-Referer": "https://github.com/Yumi-note/security-article-bot",
})
try:
    with urllib.request.urlopen(req, timeout=30) as res:
        result = json.loads(res.read())
        print("SUCCESS:", result["choices"][0]["message"]["content"])
except urllib.error.HTTPError as e:
    print(f"HTTP_ERROR_{e.code}: {e.read().decode()[:500]}")
except Exception as e:
    print(f"ERROR: {e}")
