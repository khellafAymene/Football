import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from ANIS_HAJJAJI import *
import matplotlib.font_manager as fm
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

font_italic = None  # ← لم يعد هناك خط خارجي، ونعتمد على الخط الافتراضي أعلاه

#─────0. تحديد القيم────────────────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

# خاص بألوان اللاعبين 1
Player1_color = "#FF9300"                             # لون اللاعب الأول
Player2_color = "#1A78CF"                             # لون اللاعب الثاني

# خاص بالعنوان 2
First_tittel = "Anis"                                   # العنوان الرئيسي
First_tittel_color = "#570101"                        # لون العنوان الرئيسي
First_tittel_size = 12                                  # حجم العنوان الرئيسي
First_tittel_bold = "bold"                              # سمك العنوان الرئيسي ولإزالة السمك غيرها إلى First_tittel_bold = None
fontstyle = font_italic

# خاص بالاحصائيات 3
Metric_size = 9                                         # حجم خط الاحصائيات
Metric_color = "black"                                  # لون خط الاحصائيات
Metric_bold = "bold"                                    # سمك خط الاحصائيات ولإزالة السمك غيرها إلى Metric_bold = None
Metric_distance = 108                                   # بعد الاحصائيات عن الدائرة
Metric_color_option = False                             # لكي تأخذ الإحصائيات لون الفئة الخاص بها غيرها إلى Metric_color_option = True

# خاص بالقيم 4
fact = 0.25                                             # نسبة إزاحة القيم نحو الحافة
Metric_Value_size = 8                                   # حجم خط القيم
Metric_Value_color_text = "#000000"                   # لون خط القيم
Metric_Value_bold = "bold"                              # سمك خط القيم ولإزالة السمك غيرها إلى Metric_Value_bold = None
Metric_Value_color_background_light = 0.25              # شفافية خلفية مربع القيم
Metric_Value_box_pad = 0.25                             # حجم مربع القيم
Metric_Value_box_edgecolor = "#000000"                # لون إطار مربع القيم

# خاص بإعدادات الشكل 5 
Circle_size = 4                                         # حجم الدائرة الداخلية
background = "#FFFFFF"                                # لون الخلفية
line_color = "#000000"                                # لون الخطوط الداخلية
Length = 8                                              # طول إطار الشكل
Width  = 8                                              # عرض إطار الشكل

# خاص بالمفتاح 6
legend_text_size = 7                                    # حجم خط نص المفتاح
legend_text_bold = None                                 # سمك خط المفتاح ولإظهار السمك غيرها إلى legend_text_bold = "bold"
legend_color_option = True                              # لكي تأخذ المفاتيح لون الأسود غيرها إلى Metric_color_option = False

#  تحديد أسماء الأعمدة 7
dataset = dataset.rename(columns={

# غير الأسماء في الجهة اليسرى حسب الجدول الذي عندك   
    "PLAYER"            : "PLAYER",
    "METRIC"            : "METRIC",
    "VALUE"             : "VALUE",
    "MAX"               : "MAX",
    "CATEGORY"          : "CATEGORY",
    "COLOR"             : "COLOR",

})

#─────1. تجميع البيانات─────────────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

# استخراج اللاعبين بدون تكرار
selected_players = dataset["PLAYER"].unique()

if len(selected_players) >= 2:

    # اختيار اللاعب الأول والثاني من القائمة
    player1 = selected_players[0]
    player2 = selected_players[1]

    # تخزين بيانات اللاعب الأول
    data1   = dataset[dataset["PLAYER"] == player1].sort_values(by="CATEGORY")
    values1 = data1["VALUE"].apply(percent_to_number).tolist()  # ← قيم اللاعب الأول (يدعم صيغة النسبة المئوية أيضاً)

    # تخزين بيانات اللاعب الثاني
    data2   = dataset[dataset["PLAYER"] == player2].sort_values(by="CATEGORY")
    values2 = data2["VALUE"].apply(percent_to_number).tolist()  # ← قيم اللاعب الثاني (يدعم صيغة النسبة المئوية أيضاً)

    # بيانات مشتركة بين اللاعبين
    metrics  = data1["METRIC"].astype(str).tolist()          # ← قائمة أسماء الإحصائيات
    colors   = data1["COLOR"].astype(str).str.strip().tolist()           # ← قائمة الألوان
    Max      = data1["MAX"].tolist()                         # ← قائمة الحد الأقصى
    Max_data = dict(zip(metrics, Max))                       # ← قاموس (إحصائية → حد أقصى)

#─────2. تصميم الشكل────────────────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

    # حساب عدد الاحصائيات
    N = len(metrics)

    # حساب الزوايا لكل إحصائية
    angles = np.linspace(0, 2*np.pi, N+1)

    # رسم المخطط
    fig, ax = plt.subplots(figsize=(Width, Length), subplot_kw=dict(polar=True), dpi=600)

    # إعدادات محور المخطط
    ax.set_ylim(0, 110)                                           # ← تحديد نطاق المحور
    ax.set_xticks([])                                             # ← إخفاء علامات المحور الأفقي
    ax.set_yticks([20, 40, 60, 80, 100])                          # ← تحديد علامات المحور العمودي
    ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=0)  # ← إخفاء أرقام المحور العمودي

    # إخفاء خط الدائرة الخارجية
    ax.spines["polar"].set_visible(False)

    # إخفاء الدوائر الداخلية للمخطط
    ax.grid(False)

    # رسم الدائرة الخارجية للمخطط
    theta = np.linspace(0, 2*np.pi, 500)
    ax.plot(theta, [100 + Circle_size]*500, color="black", linewidth=1.2)  # ← الدائرة الخارجية

    # رسم الدائرة الداخلية للمخطط
    ax.plot(theta, [Circle_size]*500, color="black", linewidth=0.7)        # ← الدائرة الداخلية

    # رسم الخطوط الفاصلة بين الإحصائيات
    for angle in angles[:-1]:
        ax.plot(
            [angle, angle],                        # ← اتجاه الخط (من الداخل للخارج)
            [Circle_size, 100 + Circle_size],      # ← نطاق الخط
            color=line_color,                      # ← لون الخط
            linestyle="-",                         # ← نوع الخط
            linewidth=1                            # ← سُمك الخط
        )

    # خلفية الشكل
    fig.patch.set_facecolor(background)            # ← لون خلفية الصورة

    # خلفية المحاور
    ax.set_facecolor(background)                   # ← لون خلفية المحاور

#─────3. رسم الأجزاء وكتابة القيم───────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

    # رسم الأجزاء لكل إحصائية الخاصة بكلا اللاعبين
    for i in range(N):
        # تخزين لون الفئة
        base_color = colors[i]

        # حساب الزاوية لكل فئة
        start_angle = angles[i]
        end_angle   = angles[i+1]
        mid_angle   = (start_angle + end_angle) / 2

        # رسم الجزء الخارجي (الخلفية)
        ax.bar(
            mid_angle,                         # ← زاوية المنتصف
            100,                               # ← ارتفاع الشريط
            width=end_angle - start_angle,     # ← عرض الشريط
            color=background,                  # ← لون الخلفية
            edgecolor=line_color,              # ← لون الفواصل
            bottom=Circle_size                 # ← بداية الشريط من الدائرة الداخلية
        )

        # إزالة النسبة المئوية وحساب القيم النسبية
        val1     = values1[i]
        val2     = values2[i]
        new_val1 = (val1 / Max_data[metrics[i]]) * 100   # ← القيمة النسبية للاعب الأول
        new_val2 = (val2 / Max_data[metrics[i]]) * 100   # ← القيمة النسبية للاعب الثاني
        offset   = (end_angle - start_angle) * fact       # ← مقدار إزاحة النص

        offset_max = offset
        offset_min = offset

        # تحديد القيمة الأكبر والأصغر بين اللاعبين
        if val1 >= val2:
            Max       = val1
            Min       = val2
            new_Max   = new_val1
            new_Min   = new_val2
            Color_Max = Player1_color              # ← لون اللاعب الأكبر قيمةً
            Color_Min = Player2_color              # ← لون اللاعب الأصغر قيمةً
            offset_max *= -1
        else:
            Max       = val2
            Min       = val1
            new_Max   = new_val2
            new_Min   = new_val1
            Color_Max = Player2_color              # ← لون اللاعب الأكبر قيمةً
            Color_Min = Player1_color              # ← لون اللاعب الأصغر قيمةً
            offset_min *= -1

        note_max = f"{Max:02.0f}"
        note_min = f"{Min:02.0f}"

        # رسم الجزء الداخلي (القيمة الأكبر)
        ax.bar(
            mid_angle,                         # ← زاوية المنتصف
            new_Max,                           # ← ارتفاع الشريط (القيمة الأكبر)
            width=end_angle - start_angle,     # ← عرض الشريط
            color=Color_Max,                   # ← لون اللاعب الأكبر
            edgecolor=line_color,              # ← لون الفواصل
            bottom=Circle_size                 # ← بداية الشريط من الدائرة الداخلية
        )

        # كتابة قيمة اللاعب الأكبر
        ax.text(
            mid_angle + offset_max,             # ← الموضع الأفقي مع الإزاحة
            new_Max,                            # ← الموضع العمودي
            note_max,                           # ← النص المعروض
            ha="center",                        # ← محاذاة أفقية في المنتصف
            va="center",                        # ← محاذاة عمودية في المنتصف
            fontsize=Metric_Value_size,         # ← حجم الخط
            fontweight=Metric_Value_bold,       # ← سُمك الخط
            color=Metric_Value_color_text,      # ← لون النص
            fontproperties=fontstyle,           # ← نوع الخط
            bbox=dict(
                facecolor=make_lighter(Color_Max, Metric_Value_color_background_light),  # ← لون خلفية المربع
                edgecolor=Metric_Value_box_edgecolor,                                    # ← لون إطار المربع
                boxstyle=f"round,pad={Metric_Value_box_pad}"                             # ← شكل المربع
            )
        )

        # رسم الجزء الداخلي (القيمة الأصغر)
        ax.bar(
            mid_angle,                         # ← زاوية المنتصف
            new_Min,                           # ← ارتفاع الشريط (القيمة الأصغر)
            width=end_angle - start_angle,     # ← عرض الشريط
            color=Color_Min,                   # ← لون اللاعب الأصغر
            edgecolor=line_color,              # ← لون الفواصل
            bottom=Circle_size                 # ← بداية الشريط من الدائرة الداخلية
        )

        # كتابة قيمة اللاعب الأصغر
        ax.text(
            mid_angle + offset_min,             # ← الموضع الأفقي مع الإزاحة
            new_Min,                            # ← الموضع العمودي
            note_min,                           # ← النص المعروض
            ha="center",                        # ← محاذاة أفقية في المنتصف
            va="center",                        # ← محاذاة عمودية في المنتصف
            fontsize=Metric_Value_size,         # ← حجم الخط
            fontweight=Metric_Value_bold,       # ← سُمك الخط
            color=Metric_Value_color_text,      # ← لون النص
            fontproperties=fontstyle,           # ← نوع الخط
            bbox=dict(
                facecolor=make_lighter(Color_Min, Metric_Value_color_background_light),  # ← لون خلفية المربع
                edgecolor=Metric_Value_box_edgecolor,                                    # ← لون إطار المربع
                boxstyle=f"round,pad={Metric_Value_box_pad}"                             # ← شكل المربع
            )
        )

        # حساب زاوية دوران اسم الإحصائية
        rotation_angle = np.degrees(mid_angle) + 90
        if 0 < np.degrees(mid_angle) < 180:
            rotation_angle += 180                            # ← تصحيح اتجاه النص في النصف السفلي

        # تحديد لون اسم الإحصائية بناءً على الخيار المحدد
        if Metric_color_option == True:
            Metric_color = base_color                        # ← استخدام لون الفئة

        # كتابة اسم الإحصائية
        ax.text(
            mid_angle,                                       # ← الموضع الأفقي (الزاوية)
            Metric_distance + Circle_size,                   # ← الموضع العمودي (خارج المخطط)
            auto_split(metrics[i], max_len=12),              # ← النص (مع تقسيم تلقائي)
            ha="center",                                     # ← محاذاة أفقية في المنتصف
            va="center",                                     # ← محاذاة عمودية في المنتصف
            fontsize=Metric_size,                            # ← حجم الخط
            fontweight=Metric_bold,                          # ← سُمك الخط
            rotation=rotation_angle,                         # ← زاوية دوران النص
            rotation_mode="anchor",                          # ← وضع الدوران
            color=Metric_color,                              # ← لون النص
            fontproperties=fontstyle                         # ← نوع الخط
        )

#─────4. العنوان والمفتاح───────────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

    # كتابة العنوان الرئيسي
    fig.text(
        0.515, 0.965,                  # ← موضع النص (أفقي، عمودي)
        First_tittel,                  # ← نص العنوان
        size=First_tittel_size,        # ← حجم الخط
        ha="center",                   # ← محاذاة أفقية في المنتصف
        color=First_tittel_color,      # ← لون النص
        fontweight=First_tittel_bold,  # ← سُمك النص
        fontproperties=fontstyle       # ← نوع الخط
    )

    # تجهيز قائمة اللاعبين وألوانهم لمفتاح المخطط
    categories = [
        (player1, Player1_color),      # ← اسم ولون اللاعب الأول
        (player2, Player2_color)       # ← اسم ولون اللاعب الثاني
    ]

    # إنشاء عناصر المفتاح بناءً على اللاعبين والألوان
    legend_handles = [
        plt.Line2D([0], [0], color="none", label=label)  # ← عنصر مفتاح بدون خط
        for label, _ in categories
    ]
    # تعريف خط المفتاح مع الحجم والسمك (باستخدام الخط الافتراضي فقط)
    legend_font = fm.FontProperties()
    legend_font.set_size(legend_text_size)
    legend_font.set_weight(legend_text_bold)

    # عرض المفتاح
    legend = fig.legend(
        handles=legend_handles,              # ← عناصر المفتاح
        loc='upper center',                  # ← موضع المفتاح
        bbox_to_anchor=(0.5, 0.96),          # ← إحداثيات المفتاح
        ncol=len(categories),                # ← عدد الأعمدة
        frameon=False,                       # ← إخفاء إطار المفتاح
        prop=legend_font,                    # ← نوع الخط مع الحجم والسمك
        columnspacing=0                      # ← المسافة بين الأعمدة
    )

    # ضبط لون النص في المفتاح ليتناسب مع الألوان المستخدمة
    if legend_color_option:
        for text, (_, color) in zip(legend.get_texts(), categories):
            text.set_color(color)            # ← تطبيق لون اللاعب على النص

#─────5. إظهار الرسم────────────────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────



fig.subplots_adjust(top=0.85, bottom=0.1, left=0.1, right=0.90)
plt.show()
