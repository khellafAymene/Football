# ─── استيراد المكتبات ──────────────────────────────────────────────────────────

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import warnings
warnings.filterwarnings('ignore')
# 1. استيراد المكتبات
import arabic_reshaper
from bidi.algorithm import get_display

# 2. تحديد الخط والتخلص من مشاكل إشارة السالب
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Calibri', 'Segoe UI', 'Tahoma', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

df = dataset.copy()
# 3. إعداد المشكل لحل مشكلة المربعات (تعطيل الـ ligatures)
reshaper = arabic_reshaper.ArabicReshaper(configuration={
    'delete_harakat': True,
    'support_ligatures': False
})

# 4. دالة معالجة النصوص
def ar(text):
    if not text:
        return ""
    return get_display(reshaper.reshape(str(text)))

# ─────0. تحديد القيم────────────────────────────────────────────────────────────




# 1 العناوين

Title_left = "أقوى فريق"				             # العنوان الأيسر (أصبح الأفضل على اليسار)
Title_size_left = 15                         # حجم العنوان الأيسر
Title_bold_left = None                      # سمك العنوان الأيسر ولتفعيلها السمك غيرها إلى Title_bold_left = "bold"
Title_color_left = "#999999"              # لون كتابة العنوان الأيسر

Title_right = "أضعف فريق"             # العنوان الرئيسي (أصبح الأسوأ على اليمين)
Title_size_right = 15                        # حجم العنوان الرئيسي
Title_bold_right = None                     # سمك العنوان الرئيسي ولتفعيلها السمك غيرها إلى Title_bold_right = "bold"
Title_color_right = "#999999"             # لون كتابة العنوان الرئيسي

# 2 المؤشرات

Metric_size = 15                           # حجم المؤشرات
Metric_bold = None                          # سمك المؤشرات ولتفعيلها Metric_bold = "bold"
Metric_color = "#333333"                  # لون كتابة المأشرات

# 3 خاص بإعدادات الشكل
row_height = 0.63                 # إرجاع المسافة الأصلية لعدم الحاجة للإزاحة العمودية
fig_width  = 9                  # عرض الشكل بالإنش

# 4 خاص بألوان المخطط
COLOR_DOT      = "#C8C8C8"   # لون النقاط العادية (الفرق الأخرى)
COLOR_BEST     = "#2ECC71"   # لون أفضل فريق  (أعلى قيمة)
COLOR_WORST    = "#E74C3C"   # لون أسوأ فريق  (أدنى قيمة)
COLOR_BG       = "#FFFFFF"   # لون خلفية المخطط
COLOR_LABEL    = "#333333"   # لون النصوص



#-----------------------------------------------------------------------------------
# حدود موضع النقاط أفقياً (بين 8% و92% من عرض الرسم)
x_start = 0.08
x_end   = 0.92
x_range = x_end - x_start

# ─── إعدادات حل التداخل ───────────────────────────────────────────────────────
LOGO_WIDTH = 0.1   # عتبة المسافة بين شعارين لاعتبارهما "متداخلَين"
Y_OFFSET   = 0   # مقدار الإزاحة العمودية عند التداخل


# ─────1. تجهيز الشعارات─────────────────────────────────────────────────────────

_logo_cache = {}

def preload_logos(url_list, size=(28, 28)):
    """تحميل جميع الشعارات مرة واحدة في البداية"""
    for url in url_list:
        if url in _logo_cache:
            continue
        try:
            response = requests.get(url, timeout=5)
            img = Image.open(BytesIO(response.content)).convert("RGBA")
            img = img.resize(size, Image.LANCZOS)
            _logo_cache[url] = np.array(img)
        except Exception:
            _logo_cache[url] = None


def get_logo(url):
    """إرجاع الشعار من الذاكرة فقط"""
    return _logo_cache.get(url, None)


# ─────2. قراءة البيانات─────────────────────────────────────────────────────────

url_map = dataset.drop_duplicates('TEAM').set_index('TEAM')['URL LOGO']

METRICS = dataset["METRIC"].unique()

pivot = dataset.pivot_table(
    index='TEAM',
    columns='METRIC',
    values='VALUE',
    aggfunc='first'
)
pivot.columns.name = None
pivot.index.name   = 'TEAM'
pivot.insert(0, 'URL LOGO', url_map)
pivot   = pivot.reset_index()
dataset = pivot

all_urls = dataset["URL LOGO"].unique().tolist()
preload_logos(all_urls)


# ─────3. إعداد الرسم────────────────────────────────────────────────────────────

n_metrics  = len(METRICS)
fig_height = n_metrics * row_height + 1.2

fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=300)
fig.patch.set_facecolor(COLOR_BG)
ax.set_facecolor(COLOR_BG)


# ─────4. رسم الصفوف─────────────────────────────────────────────────────────────

for row_idx, metric in enumerate(METRICS):

    y = (n_metrics - 1 - row_idx) * row_height

    col_data = dataset[["TEAM", metric, "URL LOGO"]].dropna(subset=[metric])

    if col_data.empty:
        continue

    min_val = col_data[metric].min()
    max_val = col_data[metric].max()
    rng     = max_val - min_val if max_val != min_val else 1

    best_team  = col_data.loc[col_data[metric].idxmax(), "TEAM"]
    worst_team = col_data.loc[col_data[metric].idxmin(), "TEAM"]

    # ─── جمع جميع الفرق مع تمييز الأفضل والأسوأ ───────────────────────────────
    all_teams = []

    for _, row in col_data.iterrows():
        team = row["TEAM"]
        val  = row[metric]
        url  = row["URL LOGO"]

        # تم عكس الاتجاه: القيمة الأعلى تقع الآن بالقرب من x_start (اليسار)
        # والقيمة الأدنى تقع بالقرب من x_end (اليمين) -> ترتيب من اليمين إلى اليسار
        xnorm = x_start + (1 - ((val - min_val) / rng)) * x_range

        is_best  = (team == best_team)
        is_worst = (team == worst_team)

        if is_best:
            color = COLOR_BEST
        elif is_worst:
            color = COLOR_WORST
        else:
            color = COLOR_LABEL

        all_teams.append({
            "team": team, "val": val, "url": url,
            "xnorm": xnorm, "color": color,
            "is_special": is_best or is_worst
        })

    # ─── رسم جميع العناصر (بدون معالجة تداخل) ─────────────────────────────────
    for item in all_teams:
        xnorm = item["xnorm"]
        y_actual = y

        logo = get_logo(item["url"])
        if logo is not None:
            # الأفضل/الأسوأ بحجم أكبر قليلاً وقيمة رقمية ملوّنة فوقها
            zoom = 0.8 if item["is_special"] else 0.6
            img_box = OffsetImage(logo, zoom=zoom)
            ab = AnnotationBbox(img_box, (xnorm, y_actual),
                                frameon=False, zorder=5)
            ax.add_artist(ab)

            if item["is_special"]:
                ax.text(xnorm, y_actual + 0.2,
                        f"{item['val']:.2f}",
                        ha="center", va="bottom",
                        fontsize=7.5, fontweight="bold",
                        color=item["color"], zorder=6)
        else:
            size = 120 if item["is_special"] else 55
            ax.scatter(xnorm, y_actual, s=size, color=item["color"] if item["is_special"] else COLOR_DOT,
                    zorder=5, edgecolors="white", linewidths=1 if item["is_special"] else 0.5,
                    alpha=1 if item["is_special"] else 0.75)


    # اسم المقياس على اليسار
    ax.text(-0.01, y,metric,
        ha="right", va="center",
        fontsize=Metric_size, color=Metric_color,fontweight=Metric_bold,
        transform=ax.get_yaxis_transform())


# ─────5. رأس المخطط─────────────────────────────────────────────────────────────


ax.text(x_start, 1.01, Title_left,
        ha="left", va="bottom", fontsize=Title_size_left, color=Title_color_left,fontweight=Title_bold_left,
         transform=ax.transAxes)

ax.text(x_end, 1.01, Title_right,
        ha="right", va="bottom", fontsize=Title_size_right, color=Title_color_right,fontweight=Title_bold_right,
    transform=ax.transAxes)

# ─────6. تنظيف المحاور وحفظ الملف──────────────────────────────────────────────

ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.8, (n_metrics - 1) * row_height + 0.8)
ax.axis("off")

plt.tight_layout()
plt.show()
plt.close(fig)