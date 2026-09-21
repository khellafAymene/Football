
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import numpy as np
from matplotlib.colors import to_rgba

# الاعتماد على خط عربي متوفر في النظام (بدون ملف خط خارجي)
import matplotlib.font_manager as fm

FONT_PATH = r"D:\\font\\Alexandria-Regular.ttf"   # الخط المحلي

try:
    fm.fontManager.addfont(FONT_PATH)
    custom = fm.FontProperties(fname=FONT_PATH).get_name()
except Exception:
    custom = None                          # يكمل بالخطوط الافتراضية

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ([custom] if custom else []) + ['Segoe UI', 'Tahoma', 'Arial']
plt.rcParams['axes.unicode_minus'] = False
font_italic = None

#─────0. تحديد القيم────────────────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────
# خاص بالعنوان الرئيسي 1
First_tittel="Anis"                                     # العنوان الرئيسي
First_tittel_color = "#FFFFFF"                        # لون العنوان الرئيسي
First_tittel_size = 18                                  # حجم العنوان الرئيسي
First_tittel_bold = "bold"                              # سمك العنوان الرئيسي ولإزالة السمك غيرها إلى First_tittel_bold = None
fontstyle = font_italic

# خاص بالعنوان الفرعي 2
Seconed_tittel="Anis"                                   # العنوان الفرعي
Seconed_tittel_color = "#FFFFFF"                      # لون العنوان الفرعي
Seconedtittel_size = 14                                 # حجم العنوان الفرعي
Seconed_tittel_bold = "bold"                            # سمك العنوان الفرعي ولإزالة السمك غيرها إلى First_tittel_bold = None

# خاص  بالخطوط 3
MIN_TRANSPARENCY = 0.1                                  # أقل شفافية للخط
MAX_LINE_WIDTH = 12                                     # أكبر سمك للخط
color_link = "#FFFFFF"                                # لون الخطوط بين اللاعبين

# خاص بالدائرة الخارجية 4
MAX_MARKER_SIZE = 3000                                  # أكبر حجم للدائرة
color_circle_out = "#000000"                          # لون الدوائر الخارجية
color_edgecolors_circle_out = "#000000"               # لون محيط الدائرة الخارجية
linewidth_circle_out = 1                                # سمك محيط الدائرة الخارجية

# خاص بالدائرة داخلية 5
color_circle_in = "#FD0A0A"                           # لون الدوائر الداخلية
color_edgecolors_circle_in = "#000000"                # لون محيط الدائرة الداخلية
linewidth_circle_in = 1                                 # سمك محيط الدائرة الداخلية
circle_fact = 0.85                                      # النسبة المئوية لحجم الدائرة الداخلية

# خاص بالكتابة الموجودة داخل الدائرة 6
text_color = "#FFFFFF"                                # لون رقم الرلاعب
text_size = 14                                          # حجم رقم الرلاعب
text_bold = "bold"                                      # سمك رقم الرلاعب ولإزالة السمك غيرها إلى text_bold = None

# خاص بالملعب 7
Stadium_type = "wyscout"
Stadium_color = "#22312C"                             # لون الملعب
Stadium_color_line = "#FFFFFF"                        # لون خطوط الملعب
Length = 8                                              # طول إطار الشكل
Width  = 12                                             # عرض إطار الشكل
H_left=3                                                # الهامش على اليسار القيم محصورة بين (1-0)
H_right=3                                               # الهامش على اليمين القيم محصورة بين (1-0)
H_top=2                                                 # الهامش من الأعلى القيم محصورة بين (1-0)
H_bottom=2                                              # الهامش من الأسفل القيم محصورة بين (1-0)

#  تحديد أسماء الأعمدة 8
dataset = dataset.rename(columns={

# غير الأسماء في الجهة اليسرى حسب الجدول الذي عندك   
    "FROM PLAYER"                   : "FROM PLAYER",
    "X"                             : "X",
    "Y"                             : "Y",
    "TO PLAYER"                     : "TO PLAYER",
    "NUMBER OF PASSES"              : "NUMBER OF PASSES",
    "JERSEY NUMBER"                 : "JERSEY NUMBER",

})

# ── 1. تصفية البيانات ─────────────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

# تحديد الأعمدة المطلوبة لحساب المواقع
location_cols = ['FROM PLAYER', 'X', 'Y', "NUMBER OF PASSES", "JERSEY NUMBER"]
location_formation = dataset[location_cols].copy()  # ← نسخة من البيانات

# حساب المتوسط لكل لاعب (المكان + إجمالي التمريرات + رقم القميص)
average_locs_and_count = (
    location_formation
    .groupby('FROM PLAYER')
    .agg({
        'X': 'mean',              # ← متوسط الموقع الأفقي
        'Y': 'mean',              # ← متوسط الموقع العمودي
        "NUMBER OF PASSES": "sum",  # ← إجمالي تمريرات اللاعب
        "JERSEY NUMBER": "first"  # ← رقم قميص اللاعب
    }).rename(columns={"NUMBER OF PASSES": "TOTAL PASSES"})
)

# تحديد الأعمدة المطلوبة للتمريرات بين اللاعبين
location_cols2 = ['FROM PLAYER', 'TO PLAYER', 'NUMBER OF PASSES']
passes_between = dataset[location_cols2].copy()                        # ← نسخة من البيانات
passes_between = passes_between[passes_between['NUMBER OF PASSES'] > 0]  # ← تصفية الصفوف الفارغة

# دمج مواقع اللاعبين مع بيانات التمريرات
passes_between = passes_between.merge(average_locs_and_count, left_on='FROM PLAYER', right_index=True)
passes_between = passes_between.merge(average_locs_and_count, left_on='TO PLAYER', right_index=True, suffixes=['', '_end'])

# حساب سُمك الخط بين كل لاعبين بناءً على عدد التمريرات
passes_between['width'] = (passes_between["NUMBER OF PASSES"] / passes_between["NUMBER OF PASSES"].max() * MAX_LINE_WIDTH)

# تحديد حجم دائرة كل لاعب بناءً على إجمالي تمريراته
average_locs_and_count['marker_size'] = (average_locs_and_count["TOTAL PASSES"] / average_locs_and_count["TOTAL PASSES"].max() * MAX_MARKER_SIZE)

# حساب شفافية كل خط بناءً على عدد التمريرات
color = np.array(to_rgba(color_link))                                               # ← تحويل اللون إلى RGBA
color = np.tile(color, (len(passes_between), 1))                                    # ← تكرار اللون لكل خط
c_transparency = passes_between["NUMBER OF PASSES"] / passes_between["NUMBER OF PASSES"].max()  # ← نسبة الشفافية
c_transparency = (c_transparency * (1 - MIN_TRANSPARENCY)) + MIN_TRANSPARENCY       # ← تطبيق الحد الأدنى للشفافية
color[:, 3] = c_transparency                                                        # ← تعيين قيمة الشفافية في قناة Alpha

# ── 2. إنشاء الملعب ───────────────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

pitch = Pitch(
    pitch_type=Stadium_type,               # ← نوع الملعب
    pitch_color=Stadium_color,             # ← لون أرضية الملعب
    line_color=Stadium_color_line,         # ← لون خطوط الملعب
    half=False,                            # ← إظهار الملعب كاملاً
    pad_top=H_top,                         # ← هامش من الأعلى
    pad_bottom=H_bottom,                   # ← هامش من الأسفل
    pad_left=H_left,                       # ← هامش من اليسار
    pad_right=H_right,                     # ← هامش من اليمين
    goal_type='box',                       # ← إظهار المرمى بشكل مربع
)

# إنشاء الشبكة مع تخصيص أبعاد العنوان والحواشي
fig, ax = pitch.grid(
    endnote_height=0.03,   # ← ارتفاع منطقة الحاشية السفلية
    endnote_space=0,       # ← مسافة الحاشية
    figheight=12,          # ← ارتفاع الشكل
    title_height=0.08,     # ← ارتفاع منطقة العنوان
    title_space=0,         # ← مسافة العنوان
    axis=False,            # ← إخفاء المحاور
    grid_height=0.82       # ← ارتفاع منطقة الملعب
)

fig.set_size_inches(Width, Length)           # ← تحديد حجم الصورة
fig.set_facecolor(Stadium_color)     # ← تحديد لون خلفية الصورة

# ── 3. رسم خطوط التمريرات والدوائر ───────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

# رسم خطوط التمريرات بين اللاعبين
pass_lines = pitch.lines(
    passes_between["X"],      # ← نقطة البداية أفقياً
    passes_between["Y"],      # ← نقطة البداية عمودياً
    passes_between["X_end"],  # ← نقطة النهاية أفقياً
    passes_between["Y_end"],  # ← نقطة النهاية عمودياً
    lw=passes_between.width,  # ← سُمك الخط
    color=color,              # ← لون الخط مع الشفافية
    zorder=1,                 # ← طبقة الرسم (خلف الدوائر)
    ax=ax['pitch']            # ← محور الملعب
)

# رسم الدائرة الخارجية لكل لاعب
pass_nodes = pitch.scatter(
    average_locs_and_count["X"],            # ← الموقع الأفقي للاعب
    average_locs_and_count["Y"],            # ← الموقع العمودي للاعب
    s=average_locs_and_count.marker_size, # ← حجم الدائرة
    color=color_circle_out,               # ← لون الدائرة الخارجية
    edgecolors=color_edgecolors_circle_out,  # ← لون حافة الدائرة
    linewidth=linewidth_circle_out,       # ← سُمك الحافة
    alpha=1,                              # ← بدون شفافية
    ax=ax['pitch']                        # ← محور الملعب
)

# رسم الدائرة الداخلية لكل لاعب
pass_nodes = pitch.scatter(
    average_locs_and_count["X"],                      # ← الموقع الأفقي للاعب
    average_locs_and_count["Y"],                      # ← الموقع العمودي للاعب
    s=average_locs_and_count.marker_size * circle_fact,  # ← حجم الدائرة الداخلية (أصغر من الخارجية)
    color=color_circle_in,                          # ← لون الدائرة الداخلية
    edgecolors=color_edgecolors_circle_in,          # ← لون حافة الدائرة
    linewidth=linewidth_circle_in,                  # ← سُمك الحافة
    alpha=1,                                        # ← بدون شفافية
    ax=ax['pitch']                                  # ← محور الملعب
)

# كتابة رقم القميص داخل دائرة كل لاعب
for index, row in average_locs_and_count.iterrows():  # ← يمر على كل لاعب في الجدول
    pitch.annotate(
        int(row["JERSEY NUMBER"]),  # ← النص المكتوب (رقم القميص)
        xy=(row["X"], row["Y"]),         # ← موضع الكتابة (مكان اللاعب)
        c=text_color,              # ← لون النص
        va='center',               # ← محاذاة عمودية في المنتصف
        ha='center',               # ← محاذاة أفقية في المنتصف
        size=text_size,            # ← حجم النص
        weight=text_bold,          # ← سُمك النص
        #fontname=fontstyle,         # ← نوع الخط
        fontproperties=fontstyle,
        ax=ax['pitch']             # ← محور الملعب
    )

# ── 4. العنوان الرئيسي والفرعي ───────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

# كتابة العنوان الرئيسي
ax['title'].text(
    0.5, 0.7,                           # ← موضع النص (أفقي، عمودي)
    First_tittel,                       # ← نص العنوان
    fontsize=First_tittel_size,         # ← حجم الخط
    color=First_tittel_color,           # ← لون النص
    fontweight=First_tittel_bold,       # ← سُمك النص
    ha='center',                        # ← محاذاة أفقية في المنتصف
    va='center',                        # ← محاذاة عمودية في المنتصف
    transform=ax['title'].transAxes,    # ← إحداثيات نسبية للمحور
    #fontname=fontstyle          # ← نوع الخط
    fontproperties=fontstyle
)

# كتابة العنوان الفرعي
ax['title'].text(
    0.5, 0.2,                           # ← موضع النص (أفقي، عمودي)
    Seconed_tittel,                     # ← نص العنوان الفرعي
    fontsize=Seconedtittel_size,        # ← حجم الخط
    color=Seconed_tittel_color,         # ← لون النص
    fontweight=Seconed_tittel_bold,     # ← سُمك النص
    ha='center',                        # ← محاذاة أفقية في المنتصف
    va='center',                        # ← محاذاة عمودية في المنتصف
    transform=ax['title'].transAxes,    # ← إحداثيات نسبية للمحور
    #fontname=fontstyle          # ← نوع الخط
    fontproperties=fontstyle
)

# ── 5. عرض الصورة ─────────────────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

fig.savefig('pass_network_green_hq.png', format='png', dpi=600,
            bbox_inches='tight', pad_inches=0.1,
            facecolor=fig.get_facecolor())          # ← حفظ الشكل بجودة عالية (600 dpi)

plt.show()  # ← عرض الرسم النهائي

