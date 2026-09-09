# ─── استيراد المكتبات ──────────────────────────────────────────────────────────

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms
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
plt.rcParams['font.sans-serif'] = [ 'Calibri','Segoe UI', 'Calibri', 'Tahoma', 'Arial']
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

Title_left = "أفضل أداء"              # العنوان الأيسر (أصبح الأفضل على اليسار)
Title_size_left = 11                         # حجم العنوان الأيسر
Title_bold_left = None                      # سمك العنوان الأيسر ولتفعيلها السمك غيرها إلى Title_bold_left = "bold"
Title_color_left = "#999999"              # لون كتابة العنوان الأيسر

Title_right = "أضعف أداء"             # العنوان الرئيسي (أصبح الأسوأ على اليمين)
Title_size_right = 11                        # حجم العنوان الرئيسي
Title_bold_right = None                     # سمك العنوان الرئيسي ولتفعيلها السمك غيرها إلى Title_bold_right = "bold"
Title_color_right = "#999999"             # لون كتابة العنوان الرئيسي

# ─── إعداد ارتفاع العنوانين فوق أول صف (الحل الجديد) ─────────────────────────
title_gap_left  = 0.40   # عدّل هذه القيمة لرفع/خفض العنوان الأيسر
title_gap_right = 0.40   # عدّل هذه القيمة لرفع/خفض العنوان الأيمن

# 2 المؤشرات

Metric_size = 12                           # حجم المؤشرات
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

# 5 خاص بالخط الفاصل بين المؤشرات
SHOW_SEPARATOR   = True        # إظهار/إخفاء الخط الفاصل بين كل إحصائية والأخرى
SEPARATOR_COLOR  = "#A7A7A7"   # لون الخط الفاصل
SEPARATOR_WIDTH  = 0.8         # سماكة الخط الفاصل
SEPARATOR_STYLE  = "-"         # نمط الخط: "-" متصل، "--" متقطع، ":" منقط

SHOW_TERTILE_LINES  = True        # إظهار/إخفاء الخطين العموديين
TERTILE_COLOR       = "#A7A7A7"   # لون الخطين
TERTILE_WIDTH       = 0.8         # سماكة الخطين
TERTILE_STYLE       = "-"        # نمط الخط: "-" متصل، "--" متقطع، ":" منقط

#-----------------------------------------------------------------------------------
# حدود موضع النقاط أفقياً (بين 8% و92% من عرض الرسم)
x_start = 0.08
x_end   = 0.92
x_range = x_end - x_start


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

    best_team  = col_data.loc[col_data[metric].idxmax(), "TEAM"]
    worst_team = col_data.loc[col_data[metric].idxmin(), "TEAM"]

    # ─── ترتيب الفرق تنازلياً حسب القيمة، ثم توزيعها بمسافات متساوية ──────────
    # بدل الاعتماد على القيمة الفعلية (val) لتحديد الموقع الأفقي، نعتمد على
    # "رتبة" الفريق بين بقية الفرق. هذا يضمن مسافة ثابتة بين كل فريقين
    # متجاورين ويمنع تداخل الشعارات عند تقارب القيم.
    sorted_data = col_data.sort_values(metric, ascending=False).reset_index(drop=True)
    n_teams = len(sorted_data)

    all_teams = []

    for rank, row in sorted_data.iterrows():
        team = row["TEAM"]
        val  = row[metric]
        url  = row["URL LOGO"]

        if n_teams > 1:
            xnorm = x_start + (rank / (n_teams - 1)) * x_range
        else:
            xnorm = (x_start + x_end) / 2

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

    # ─── رسم جميع العناصر (موزّعة بانتظام الآن) ────────────────────────────────
    for item in all_teams:
        xnorm = item["xnorm"]
        y_actual = y

        logo = get_logo(item["url"])
        if logo is not None:
            zoom = 0.8 if item["is_special"] else 0.6
            img_box = OffsetImage(logo, zoom=zoom)
            ab = AnnotationBbox(img_box, (xnorm, y_actual),
                                frameon=False, zorder=5)
            ax.add_artist(ab)

            if item["is_special"]:
                ax.text(xnorm, y_actual + 0.2,
                        f"{item['val']:.0f}",
                        ha="center", va="bottom",
                        fontsize=7.5, fontweight="bold",
                        color=item["color"], zorder=6)
            else:
                ax.text(xnorm, y_actual + 0.2,
                        f"{item['val']:.0f}",
                        ha="center", va="bottom",
                        fontsize=6.5,
                        color=COLOR_LABEL, zorder=6)
        else:
            size = 120 if item["is_special"] else 55
            ax.scatter(xnorm, y_actual, s=size, color=item["color"] if item["is_special"] else COLOR_DOT,
                    zorder=5, edgecolors="white", linewidths=1 if item["is_special"] else 0.5,
                    alpha=1 if item["is_special"] else 0.75)


    # اسم المقياس على اليسار
    ax.text(0.95, y, metric,
    ha="left", va="center",
    fontsize=Metric_size, color=Metric_color, fontweight=Metric_bold,
    transform=ax.get_yaxis_transform())

# ─────4ب. رسم الخطوط الفاصلة بين المؤشرات─────────────────────────────────────
if SHOW_SEPARATOR:
    # transform مختلط: x بإحداثيات المحور (axes fraction)، y بإحداثيات البيانات
    trans_separator = mtransforms.blended_transform_factory(ax.transAxes, ax.transData)

    separator_x_end = 1.50   # عدّل هذه القيمة لتتحكم بمدى امتداد الخط تحت اسم المؤشر

    for row_idx in range(n_metrics - 1):
        y_current = (n_metrics - 1 - row_idx) * row_height
        y_next    = (n_metrics - 1 - (row_idx + 1)) * row_height
        y_mid     = (y_current + y_next) / 2

        ax.plot([x_start, separator_x_end], [y_mid + 0.05, y_mid + 0.05],
                color=SEPARATOR_COLOR, linewidth=SEPARATOR_WIDTH,
                linestyle=SEPARATOR_STYLE, zorder=1,
                transform=trans_separator, clip_on=False)

# ─────4ج. رسم خطين عموديين يقسمان الفرق إلى 3 مجموعات (أفضل / وسط / أضعف) ──────

SHOW_TERTILE_LINES  = True        # إظهار/إخفاء الخطين العموديين
TERTILE_COLOR       = "#A7A7A7"   # لون الخطين
TERTILE_WIDTH       = 1.0         # سماكة الخطين
TERTILE_STYLE       = "-"        # نمط الخط: "-" متصل، "--" متقطع، ":" منقط

if SHOW_TERTILE_LINES:
    total_teams = dataset['TEAM'].nunique()

    base      = total_teams // 3
    remainder = total_teams % 3

    if remainder == 0:
        sizes = [base, base, base]
    elif remainder == 1:
        sizes = [base, base + 1, base]      # الفرد الزائد يروح للوسط
    else:  # remainder == 2
        sizes = [base, base + 2, base]      # الفرديّن الزوائد يروحوا للوسط

    boundary1 = sizes[0]                 # عدد الفرق بالمجموعة الأولى (يسار)
    boundary2 = sizes[0] + sizes[1]       # نهاية المجموعة الوسطى

    def rank_to_x(rank):
        """تحويل رتبة الفريق (0-indexed) إلى موضع أفقي xnorm"""
        if total_teams > 1:
            return x_start + (rank / (total_teams - 1)) * x_range
        return (x_start + x_end) / 2

    # موضع الخط = نقطة الوسط بين آخر عنصر بمجموعة وأول عنصر بالمجموعة التالية
    x_line1 = (rank_to_x(boundary1 - 1) + rank_to_x(boundary1)) / 2
    x_line2 = (rank_to_x(boundary2 - 1) + rank_to_x(boundary2)) / 2

    y_top    = (n_metrics - 1) * row_height + max(title_gap_left, title_gap_right)
    y_bottom = -0.3

    for x_line in (x_line1, x_line2):
        ax.plot([x_line, x_line], [y_bottom, y_top],
                color=TERTILE_COLOR, linewidth=TERTILE_WIDTH,
                linestyle=TERTILE_STYLE, zorder=2)
# ─────5. رأس المخطط────────────────────────────────────────────────────────────

top_row_y = (n_metrics - 1) * row_height

trans_mixed = mtransforms.blended_transform_factory(ax.transAxes, ax.transData)

ax.text(x_start, top_row_y + title_gap_left, Title_left,
        ha="left", va="bottom", fontsize=Title_size_left, color=Title_color_left, fontweight=Title_bold_left,
        transform=trans_mixed)

ax.text(x_end, top_row_y + title_gap_right, Title_right,
        ha="right", va="bottom", fontsize=Title_size_right, color=Title_color_right, fontweight=Title_bold_right,
        transform=trans_mixed)

# ─────6. تنظيف المحاور وحفظ الملف──────────────────────────────────────────────

ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.8, (n_metrics - 1) * row_height + max(title_gap_left, title_gap_right) + 0.5)
ax.axis("off")

plt.tight_layout()
plt.show()
plt.close(fig)