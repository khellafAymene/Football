# ─── استيراد المكتبات ──────────────────────────────────────────────────────────
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# 2. تحديد الخط والتخلص من مشاكل إشارة السالب
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Tahoma', 'Arial']
plt.rcParams['axes.unicode_minus'] = False



# ─────0. تحديد القيم────────────────────────────────────────────────────────────

# 1 العناوين

Title_left = "الأداء الأقل"              # العنوان الأيسر (أصبح الأفضل على اليسار)
Title_size_left = 11                         # حجم العنوان الأيسر
Title_bold_left = None                      # سمك العنوان الأيسر ولتفعيلها السمك غيرها إلى Title_bold_left = "bold"
Title_color_left = "#999999"              # لون كتابة العنوان الأيسر

Title_right = "الأداء الأفضل"            # العنوان الرئيسي (أصبح الأسوأ على اليمين)
Title_size_right = 11                        # حجم العنوان الرئيسي
Title_bold_right = None                     # سمك العنوان الرئيسي ولتفعيلها السمك غيرها إلى Title_bold_right = "bold"
Title_color_right = "#999999"             # لون كتابة العنوان الرئيسي

# ─── إعداد ارتفاع العنوانين فوق أول صف (الحل الجديد) ─────────────────────────
title_gap_left  = 0.40   # عدّل هذه القيمة لرفع/خفض العنوان الأيسر
title_gap_right = 0.40   # عدّل هذه القيمة لرفع/خفض العنوان الأيمن

# 2 المؤشرات

Metric_size = 12                             # حجم المؤشرات
Metric_bold = None                          # سمك المؤشرات ولتفعيلها Metric_bold = "bold"
Metric_color = "#333333"                  # لون كتابة المأشرات

# 3 خاص بإعدادات الشكل
row_height = 0.63                 # إرجاع المسافة الأصلية لعدم الحاجة للإزاحة العمودية
fig_width  = 9                   # عرض الشكل بالإنش

# 4 خاص بألوان المخطط
COLOR_DOT        = "#C8C8C8"   # لون النقاط العادية (الفرق الأخرى)
COLOR_BEST       = "#2ECC71"   # لون أفضل فريق  (أعلى قيمة)
COLOR_WORST      = "#E74C3C"   # لون أسوأ فريق  (أدنى قيمة)
COLOR_SELECTED_1 = "#3498DB"   # لون الفريق المختار الأول
COLOR_SELECTED_2 = "#9B59B6"   # لون الفريق المختار الثاني
COLOR_BG         = "#FFFFFF"   # لون خلفية المخطط


# 5 خاص بالخط الفاصل بين المؤشرات
SHOW_SEPARATOR   = True        # إظهار/إخفاء الخط الفاصل بين كل إحصائية والأخرى
SEPARATOR_COLOR  = "#A7A7A7"   # لون الخط الفاصل
SEPARATOR_WIDTH  = 0.8         # سماكة الخط الفاصل
SEPARATOR_STYLE  = "-"         # نمط الخط: "-" متصل، "--" متقطع، ":" منقط


#-----------------------------------------------------------------------------------
# حدود موضع النقاط أفقياً (بين 8% و92% من عرض الرسم)
x_start = 0.08
x_end   = 0.92
x_range = x_end - x_start

# ─── إعدادات حل التداخل ───────────────────────────────────────────────────────
LOGO_WIDTH = 0.1   # عتبة المسافة بين شعارين لاعتبارهما "متداخلَين"
target_px  = 28    # الحجم الظاهري المطلوب لكل شعار بالبكسل التقريبي عند dpi=300

# ─────1. تجهيز الشعارات─────────────────────────────────────────────────────────

_logo_cache = {}

def preload_logos(url_list):
    """تحميل جميع الشعارات مرة واحدة في البداية، بأقصى دقة متاحة دون تصغير"""
    for url in url_list:
        if url in _logo_cache:
            continue
        try:
            response = requests.get(url, timeout=5)
            img = Image.open(BytesIO(response.content)).convert("RGBA")
            _logo_cache[url] = np.array(img)
        except Exception:
            _logo_cache[url] = None


def get_logo(url):
    """إرجاع الشعار من الذاكرة فقط"""
    return _logo_cache.get(url, None)


# ─────2. قراءة البيانات─────────────────────────────────────────────────────────

url_map = dataset.drop_duplicates('TEAM').set_index('TEAM')['URL LOGO']

SELECTED_TEAM_1 = dataset["SELECTED TEAM 1"][0]
SELECTED_TEAM_2 = dataset["SELECTED TEAM 2"][0]

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

fig, ax = plt.subplots(figsize=(fig_width, fig_height),dpi=600)
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

    best_val  = col_data[metric].max()
    worst_val = col_data[metric].min()

    selected1_row = col_data[col_data["TEAM"] == SELECTED_TEAM_1]
    selected2_row = col_data[col_data["TEAM"] == SELECTED_TEAM_2]
    selected_has_best_val  = False
    selected_has_worst_val = False

    for sel_row in (selected1_row, selected2_row):
        if not sel_row.empty:
            sel_val = sel_row[metric].values[0]
            if abs(sel_val - best_val) < 1e-9:
                selected_has_best_val = True
            if abs(sel_val - worst_val) < 1e-9:
                selected_has_worst_val = True

    # ─── جمع الفرق المميزة ────────────────────────────────────────────────────
    special_teams = []

    for _, row in col_data.iterrows():
        team = row["TEAM"]
        val  = row[metric]
        url  = row["URL LOGO"]

        xnorm = x_start + (((val - min_val) / rng)) * x_range

        is_best      = (team == best_team)
        is_worst     = (team == worst_team)
        is_selected1 = (team == SELECTED_TEAM_1)
        is_selected2 = (team == SELECTED_TEAM_2)
        is_selected  = is_selected1 or is_selected2

        if is_best and selected_has_best_val and not is_selected:
            continue
        if is_worst and selected_has_worst_val and not is_selected:
            continue

        if is_best or is_worst or is_selected:
            if is_selected1:
                border_color = COLOR_SELECTED_1
            elif is_selected2:
                border_color = COLOR_SELECTED_2
            elif is_best:
                border_color = COLOR_BEST
            else:
                border_color = COLOR_WORST

            special_teams.append({
                "team": team, "val": val, "url": url,
                "xnorm": xnorm, "color": border_color,
                "fixed": (is_best or is_worst)
            })
        else:
            ax.scatter(xnorm, y, s=55, color=COLOR_DOT,
                       zorder=3, edgecolors="white", linewidths=0.5, alpha=0.75)

    special_teams.sort(key=lambda t: t["xnorm"])

    n_special = len(special_teams)
    if n_special > 0:
        x_positions = [item["xnorm"] for item in special_teams]
        fixed_flags = [item["fixed"] for item in special_teams]

        for _ in range(50):
            moved = False
            for i in range(n_special - 1):
                gap = x_positions[i+1] - x_positions[i]
                if gap < LOGO_WIDTH:
                    overlap = LOGO_WIDTH - gap
                    left_fixed  = fixed_flags[i]
                    right_fixed = fixed_flags[i+1]

                    if left_fixed and right_fixed:
                        continue
                    elif left_fixed:
                        x_positions[i+1] += overlap
                    elif right_fixed:
                        x_positions[i]   -= overlap
                    else:
                        mid_overlap = (x_positions[i+1] + x_positions[i]) / 2
                        if mid_overlap < 0.5:
                            x_positions[i]   += overlap * 0.2
                            x_positions[i+1] += overlap * 0.8
                        else:
                            x_positions[i]   -= overlap * 0.8
                            x_positions[i+1] -= overlap * 0.2

                    moved = True
            if not moved:
                break

        for i in range(n_special):
            if fixed_flags[i]:
                special_teams[i]["xnorm"] = x_positions[i]
            else:
                special_teams[i]["xnorm"] = max(x_start, min(x_end, x_positions[i]))

    # ─── رسم العناصر بعد تعديل مواقعها ────────────────────────────────────────
    for item in special_teams:
        xnorm = item["xnorm"]
        y_actual = y

        logo = get_logo(item["url"])
        if logo is not None:
            zoom = target_px / logo.shape[0]
            img_box = OffsetImage(logo, zoom=zoom, resample=True)
            ab = AnnotationBbox(img_box, (xnorm, y_actual),
                                frameon=False, zorder=5)
            ax.add_artist(ab)
            ax.text(xnorm, y_actual + 0.2,
                    f"{item['val']:02.0f}",
                    ha="center", va="bottom",
                    fontsize=7.5, fontweight="bold",
                    color=item["color"], zorder=6)
        else:
            ax.scatter(xnorm, y_actual, s=120, color=item["color"],
                    zorder=5, edgecolors="white", linewidths=1)


    ax.text(0.95, y, metric,
    ha="left", va="center",
    fontsize=Metric_size, color=Metric_color, fontweight=Metric_bold,
    transform=ax.get_yaxis_transform())

# ─────4ب. رسم الخطوط الفاصلة بين المؤشرات─────────────────────────────────────
if SHOW_SEPARATOR:
    # transform مختلط: x بإحداثيات المحور (axes fraction)، y بإحداثيات البيانات
    trans_separator = mtransforms.blended_transform_factory(ax.transAxes, ax.transData)

    separator_x_end = 30   # عدّل هذه القيمة لتتحكم بمدى امتداد الخط تحت اسم المؤشر

    for row_idx in range(n_metrics - 1):
        y_current = (n_metrics - 1 - row_idx) * row_height
        y_next    = (n_metrics - 1 - (row_idx + 1)) * row_height
        y_mid     = (y_current + y_next) / 2

        ax.plot([x_start, separator_x_end], [y_mid + 0.05, y_mid + 0.05],
                color=SEPARATOR_COLOR, linewidth=SEPARATOR_WIDTH,
                linestyle=SEPARATOR_STYLE, zorder=1,
                transform=trans_separator, clip_on=False)
# ─────5. رأس المخطط─────────────────────────────────────────────────────────────

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


fig.subplots_adjust(top=1, bottom=0.0, left=0.0, right=0.90)
plt.show()
