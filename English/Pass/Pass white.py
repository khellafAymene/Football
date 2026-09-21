
import matplotlib.pyplot as plt
from mplsoccer import Pitch


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
First_tittel = "Anis"                                   # العنوان الرئيسي
First_tittel_color = "#000000"                        # لون العنوان الرئيسي
First_tittel_size = 18                                  # حجم العنوان الرئيسي
First_tittel_bold = "bold"                              # سمك العنوان الرئيسي ولإزالة السمك غيرها إلى First_tittel_bold = None
fontstyle = font_italic

# خاص بالعنوان الفرعي 2
Seconed_tittel = "Anis"                                 # العنوان الفرعي
Seconed_tittel_color = "#000000"                      # لون العنوان الفرعي
Seconedtittel_size = 14                                 # حجم العنوان الفرعي
Seconed_tittel_bold = "bold"                            # سمك العنوان الفرعي ولإزالة السمك غيرها إلى Seconed_tittel_bold = None

# خاص بالتمريرات 3
option = 2                                             # نوع الرسم: 1 = خطوط، 2 = أسهم
color_complete = "#ad993c"                            # لون التمريرات الناجحة
color_incomplete = "#ba4f45"                          # لون التمريرات الفاشلة

# خاص بالملعب 4
Stadium_color = "#FFFFFF"                             # لون الملعب
Stadium_color_line = "#000000"                        # لون خطوط الملعب
H_left = 3.5                                            # الهامش على اليسار القيم محصورة بين (1-0)
H_right = 3.5                                           # الهامش على اليمين القيم محصورة بين (1-0)
H_top = 2.5                                             # الهامش من الأعلى القيم محصورة بين (1-0)
H_bottom = 2                                            # الهامش من الأسفل القيم محصورة بين (1-0)

# خاص الشكل 5
Length = 7.3                                              # طول إطار الشكل
Width  = 10                                              # عرض إطار الشكل

#  تحديد أسماء الأعمدة 6
dataset = dataset.rename(columns={

# غير الأسماء في الجهة اليسرى حسب الجدول الذي عندك   
    "EVENT"             : "EVENT",
    "X"                 : "X",
    "Y"                 : "Y",
    "END_X"             : "END_X",
    "END_Y"             : "END_Y",

})

# ── 1. تصفية البيانات ─────────────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

# تحديد فقط التمريرات الناجحة
pass_complete = dataset["EVENT"].str.upper().str.strip() == 'PASS SUCC' 

# ── 2. إنشاء الملعب ───────────────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

pitch = Pitch(
    pitch_type='wyscout',            # ← نوع الملعب
    pitch_color=Stadium_color,         # ← لون أرضية الملعب
    line_color=Stadium_color_line,     # ← لون خطوط الملعب
    half=False,                        # ← إظهار الملعب كاملاً
    pad_top=H_top,                     # ← هامش من الأعلى
    pad_bottom=H_bottom,               # ← هامش من الأسفل
    pad_left=H_left,                   # ← هامش من اليسار
    pad_right=H_right,                 # ← هامش من اليمين
    goal_type='box',                   # ← إظهار المرمى بشكل مربع
)

fig, ax = pitch.draw(figsize=(10, 7.3))  # ← رسم الملعب مع تحديد الحجم
fig.patch.set_facecolor(Stadium_color)   # ← تحديد لون خلفية الصورة

# ── 3. رسم التمريرات الناجحة ──────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

if option == 1:
    # رسم التمريرات الناجحة بشكل خطوط
    pitch.lines(
        dataset[pass_complete]["X"],        # ← نقطة البداية أفقياً
        dataset[pass_complete]["Y"],        # ← نقطة البداية عمودياً
        dataset[pass_complete]["END_X"],    # ← نقطة النهاية أفقياً
        dataset[pass_complete]["END_Y"],    # ← نقطة النهاية عمودياً
        lw=5,                            # ← سُمك الخط
        transparent=True,                # ← تفعيل الشفافية التدريجية
        comet=True,                      # ← تأثير المذنب على الخط
        color=color_complete,            # ← لون التمريرات الناجحة
        ax=ax                            # ← محور الملعب
    )
else:
    # رسم التمريرات الناجحة بشكل أسهم
    pitch.arrows(
        dataset[pass_complete]["X"],        # ← نقطة البداية أفقياً
        dataset[pass_complete]["Y"],        # ← نقطة البداية عمودياً
        dataset[pass_complete]["END_X"],    # ← نقطة النهاية أفقياً
        dataset[pass_complete]["END_Y"],    # ← نقطة النهاية عمودياً
        width=2,                         # ← عرض السهم
        headwidth=10,                    # ← عرض رأس السهم
        headlength=10,                   # ← طول رأس السهم
        color=color_complete,            # ← لون التمريرات الناجحة
        ax=ax                            # ← محور الملعب
    )

# ── 4. رسم التمريرات الفاشلة ──────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

if option == 1:
    # رسم التمريرات الفاشلة بشكل خطوط
    pitch.lines(
        dataset[~pass_complete]["X"],        # ← نقطة البداية أفقياً
        dataset[~pass_complete]["Y"],        # ← نقطة البداية عمودياً
        dataset[~pass_complete]["END_X"],    # ← نقطة النهاية أفقياً
        dataset[~pass_complete]["END_Y"],    # ← نقطة النهاية عمودياً
        lw=5,                            # ← سُمك الخط
        transparent=True,                # ← تفعيل الشفافية التدريجية
        comet=True,                      # ← تأثير المذنب على الخط
        color=color_incomplete,          # ← لون التمريرات الفاشلة
        ax=ax                            # ← محور الملعب
    )
else:
    # رسم التمريرات الفاشلة بشكل أسهم
    pitch.arrows(
        dataset[~pass_complete]["X"],        # ← نقطة البداية أفقياً
        dataset[~pass_complete]["Y"],        # ← نقطة البداية عمودياً
        dataset[~pass_complete]["END_X"],    # ← نقطة النهاية أفقياً
        dataset[~pass_complete]["END_Y"],    # ← نقطة النهاية عمودياً
        width=2,                         # ← عرض السهم
        headwidth=10,                    # ← عرض رأس السهم
        headlength=10,                   # ← طول رأس السهم
        color=color_incomplete,          # ← لون التمريرات الفاشلة
        ax=ax                            # ← محور الملعب
    )

# ── 5. العنوان الرئيسي والفرعي ───────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

# كتابة العنوان الرئيسي
ax.text(
    0.5, 1.035,                         # ← موضع النص (أفقي، عمودي)
    First_tittel,                       # ← نص العنوان
    fontsize=First_tittel_size,         # ← حجم الخط
    color=First_tittel_color,           # ← لون النص
    fontweight=First_tittel_bold,       # ← سُمك النص
    ha="center",                        # ← محاذاة أفقية في المنتصف
    transform=ax.transAxes,             # ← إحداثيات نسبية للمحور
    fontproperties=fontstyle            # ← نوع الخط
)

# كتابة العنوان الفرعي
ax.text(
    0.5, 1,                             # ← موضع النص (أفقي، عمودي)
    Seconed_tittel,                     # ← نص العنوان الفرعي
    fontsize=Seconedtittel_size,        # ← حجم الخط
    color=Seconed_tittel_color,         # ← لون النص
    fontweight=Seconed_tittel_bold,     # ← سُمك النص
    ha="center",                        # ← محاذاة أفقية في المنتصف
    transform=ax.transAxes,             # ← إحداثيات نسبية للمحور
    fontproperties=fontstyle            # ← نوع الخط
)

# ── 6. عرض الصورة ─────────────────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

plt.subplots_adjust(left=0.03, right=0.97, top=0.90, bottom=0.03)  # ← ضبط هوامش الصورة

fig.savefig('pass_white_hq.png', format='png', dpi=600,
            bbox_inches='tight', pad_inches=0.1,
            facecolor=fig.get_facecolor())          # ← حفظ الشكل بجودة عالية (600 dpi)

plt.show()  # ← عرض الرسم النهائي