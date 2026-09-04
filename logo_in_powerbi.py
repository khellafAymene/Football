import traceback
import matplotlib.pyplot as plt
import requests


# رابط نظيف وثابت بدون أي توكن في النهاية
url = "https://raw.githubusercontent.com/khellafAymene/Football/refs/heads/main/un_logo.py"

# ضع التوكن الدائم الخاص بك هنا
headers = {"Authorization": "token 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"}

res = requests.get(url, headers=headers, timeout=10)
res.raise_for_status()

# تنفيذ الكود وتمرير المتغيرات
exec(res.text, globals(), locals())
