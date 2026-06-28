import urllib.request, urllib.error, json, os

api_key = os.environ.get("GROQ_API_KEY", "")
print(f"KEY_PREFIX: {api_key[:10]}")
print(f"KEY_LENGTH: {len(api_key)}")

url = "https://api.groq.com/openai/v1/chat/completions"
body = json.dumps({
    "model": "llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": "Hi, say hello in one word"}],
    "max_tokens": 10
}).encode()

req = urllib.request.Request(url, data=body, method="POST", headers={
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
})
try:
    with urllib.request.urlopen(req, timeout=30) as res:
        result = json.loads(res.read())
        print("API_SUCCESS:", result["choices"][0]["message"]["content"])
except urllib.error.HTTPError as e:
    print(f"API_HTTP_ERROR_{e.code}: {e.read().decode()[:500]}")
except Exception as e:
    print(f"API_ERROR: {e}")
