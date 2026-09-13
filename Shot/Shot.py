import matplotlib.pyplot as plt
from mplsoccer import Pitch

# الاعتماد على خط عربي متوفر في النظام (بدون ملف خط خارجي)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Calibri', 'Tahoma', 'Segoe UI', 'Arial']
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

# تغيير مكان الشوط الأول 2
First_half="1st"                            # اسم الشوط الأول
postion_1st_x = 0.25                     # مكان الشوط الأول
postion_1st_y = 0                           # ارتفاع الشوط الأول

# تغيير مكان الشوط الثاني 3
Seconed_half="2nd"                       # اسم الشوط الثاني
postion_2nd_x = 0.75                     # مكان الشوط الثاني
postion_2nd_y = 0                           # ارتفاع الشوط الثاني

# خصائص الشوطين 4
half_color = "#FFFFFF"                      # لون العنوان الفرعي
half_size = 14                                 # حجم العنوان الفرعي
half_bold = "bold"                            # سمك العنوان الفرعي ولإزالة السمك غيرها إلى First_tittel_bold = None

# خاص بالملعب 5
arrow_color_line = "Reds"                                      # لون خط التسديدة

Stadium_color = "#22312C"                             # لون الملعب
Stadium_color_line = "#FFFFFF"                        # لون خطوط الملعب

Circle_size = 200                                       # حجم الدائرة
Circle_edgecolor = "#FFFFFF"                          # إطار الدائرة
Length = 7                                              # طول إطار الشكل
Width  = 10                                              # عرض إطار الشكل
H_left=3.5                                                # الهامش على اليسار القيم محصورة بين (1-0)
H_right=3.5                                               # الهامش على اليمين القيم محصورة بين (1-0)
H_top=3                                               # الهامش من الأعلى القيم محصورة بين (1-0)
H_bottom=2                                              # الهامش من الأسفل القيم محصورة بين (1-0)

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

# تحديد فقط الأهداف المسجلة
mask_goal = dataset["EVENT"].str.upper().str.strip() == 'GOAL'

# ── 2. إنشاء الملعب ───────────────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

pitch = Pitch(
    pitch_type='wyscout',              # ← نوع الملعب
    pitch_color=Stadium_color,         # ← لون أرضية الملعب
    line_color=Stadium_color_line,     # ← لون خطوط الملعب
    half=False,                         # ← إظهار نصف الملعب فقط
    pad_top=H_top,                     # ← هامش من الأعلى
    pad_bottom=H_bottom,               # ← هامش من الأسفل
    pad_left=H_left,                   # ← هامش من اليسار
    pad_right=H_right,                 # ← هامش من اليمين
    goal_type='box',                   # ← إظهار المرمى بشكل مربع
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

fig.set_size_inches(Width, Length)       # ← تحديد حجم الصورة
fig.set_facecolor(Stadium_color)         # ← تحديد لون خلفية الصورة

# ── 3. رسم خطوط التسديدات والدوائر ───────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

# رسم خطوط التسديدات
pitch.lines(
    dataset["X"], dataset["Y"],        # ← نقطة البداية (موقع التسديدة)
    dataset["END_X"], dataset["END_Y"], # ← نقطة النهاية (وجهة التسديدة)
    lw=5,                         # ← سُمك الخط
    transparent=True,             # ← تفعيل الشفافية التدريجية
    comet=True,                   # ← تأثير المذنب على الخط
    cmap=arrow_color_line,              # ← لون الخطوط
    ax=ax['pitch']                # ← محور الملعب
)

# رسم الأهداف المسجلة
pitch.scatter(
    dataset[mask_goal]["END_X"],     # ← الموقع الأفقي للهدف
    dataset[mask_goal]["END_Y"],     # ← الموقع العمودي للهدف
    s=Circle_size,                # ← حجم الدائرة
    marker='football',            # ← شكل كرة القدم
    edgecolors='black',           # ← لون حافة الدائرة
    c='white',                    # ← لون الدائرة
    zorder=2,                     # ← طبقة الرسم (فوق الخطوط)
    ax=ax['pitch']                # ← محور الملعب
)

# رسم التسديدات الضائعة
pitch.scatter(
    dataset[~mask_goal]["END_X"],    # ← الموقع الأفقي للتسديدة
    dataset[~mask_goal]["END_Y"],    # ← الموقع العمودي للتسديدة
    edgecolors=Circle_edgecolor,  # ← لون حافة الدائرة
    c=Stadium_color,              # ← لون الدائرة
    s=Circle_size,                # ← حجم الدائرة
    zorder=2,                     # ← طبقة الرسم (فوق الخطوط)
    ax=ax['pitch']                # ← محور الملعب
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
    fontproperties=fontstyle            # ← نوع الخط
)

ax['title'].text(
    postion_1st_x, postion_1st_y,                           # ← موضع النص (أفقي، عمودي)
    First_half,                     # ← نص العنوان الفرعي
    fontsize=half_size,        # ← حجم الخط
    color=half_color,         # ← لون النص
    fontweight=half_bold,     # ← سُمك النص
    ha='center',                        # ← محاذاة أفقية في المنتصف
    va='center',                        # ← محاذاة عمودية في المنتصف
    transform=ax['title'].transAxes,    # ← إحداثيات نسبية للمحور
    fontproperties=fontstyle            # ← نوع الخط
)
ax['title'].text(
    postion_2nd_x, postion_2nd_y,                           # ← موضع النص (أفقي، عمودي)
    Seconed_half,                     # ← نص العنوان الفرعي
    fontsize=half_size,        # ← حجم الخط
    color=half_color,         # ← لون النص
    fontweight=half_bold,     # ← سُمك النص
    ha='center',                        # ← محاذاة أفقية في المنتصف
    va='center',                        # ← محاذاة عمودية في المنتصف
    transform=ax['title'].transAxes,    # ← إحداثيات نسبية للمحور
    fontproperties=fontstyle            # ← نوع الخط
)
# ── 5. عرض الصورة ─────────────────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

fig.savefig('shot_map_hq.png', format='png', dpi=600,
            bbox_inches='tight', pad_inches=0.1,
            facecolor=fig.get_facecolor())          # ← حفظ الشكل بجودة عالية (600 dpi)

plt.show()  # ← عرض الرسم النهائي