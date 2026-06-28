import urllib.request, urllib.error, json, os

api_key = os.environ.get("GEMINI_API_KEY", "")
print(f"キー先頭: {api_key[:15]}... 長さ: {len(api_key)}")

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
body = json.dumps({"contents": [{"parts": [{"text": "Hi"}]}]}).encode()

req = urllib.request.Request(url, data=body, method="POST", headers={
    "Content-Type": "application/json",
    "X-goog-api-key": api_key,
})

try:
    with urllib.request.urlopen(req, timeout=30) as res:
        result = json.loads(res.read())
        print("SUCCESS:", result["candidates"][0]["content"]["parts"][0]["text"])
except urllib.error.HTTPError as e:
    print(f"HTTP_ERROR {e.code}: {e.read().decode()[:500]}")
except Exception as e:
    print(f"ERROR: {e}")
