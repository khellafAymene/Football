import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from ANIS_HAJJAJI import *
# 1. استيراد المكتبات الخاصة بدعم اللغة العربية
import arabic_reshaper
from bidi.algorithm import get_display

# 2. تحديد الخطوط التي تدعم العربية والتخلص من مشاكل إشارة السالب
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Calibri', 'Tahoma', 'Segoe UI', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# 3. إعداد المشكل لحل مشكلة المربعات (تعطيل الـ ligatures)
reshaper = arabic_reshaper.ArabicReshaper(configuration={
    'delete_harakat': True,
    'support_ligatures': False
})

# 4. دالة معالجة النصوص العربية
def ar(text):
    if not text:
        return ""
    return get_display(reshaper.reshape(str(text)))

#─────0. تحديد القيم────────────────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────
Max_players = dataset["RANK"].max()           # أقصى عدد للاعبين في الترتيب

# خاص بالعنوان الرئيسي 1
First_tittel = "Anis"                                   # العنوان الرئيسي
First_tittel_color = "#570101"                        # لون العنوان الرئيسي
First_tittel_size = 12                                  # حجم العنوان الرئيسي
First_tittel_bold = "bold"                              # سمك العنوان الرئيسي ولإزالة السمك غيرها إلى First_tittel_bold = None

# خاص بالاحصائيات 2
Metric_size = 9                                         # حجم خط الاحصائيات
Metric_color = "black"                                  # لون خط الاحصائيات
Metric_bold = "bold"                                    # سمك خط الاحصائيات ولإزالة السمك غيرها إلى Metric_bold = None
Metric_distance = 108                                   # بعد الاحصائيات عن الدائرة
Metric_color_option = False                             # لكي تأخذ الإحصائيات لون الفئة الخاص بها غيرها إلى Metric_color_option = True

# خاص بالقيم 3
Metric_Value_size = 8                                   # حجم خط القيم
Metric_Value_color_text = "black"                     # لون خط القيم
Metric_Value_bold = "bold"                              # سمك خط القيم ولإزالة السمك غيرها إلى Metric_Value_bold = None
Metric_Value_color_background_light = 0.25              # شفافية خلفية مربع القيم
Metric_Value_box_pad = 0.2                              # حجم مربع القيم
Metric_Value_box_edgecolor = "black"                  # لون إطار مربع القيم

# خاص بإعدادات الشكل 4
Circle_size = 10                                      # حجم الدائرة الداخلية
out_color_light = 0.8                                   # شفافية لون الجزء الخارجي
background = "#FFFFFF"                                # لون الخلفية
line_color = "white"                                  # لون الخطوط الداخلية
Length = 8                                              # طول إطار الشكل
Width  = 8                                              # عرض إطار الشكل

# خاص بالمفتاح 5
legend_text_size = 7                                    # حجم خط نص المفتاح
legend_text_bold = None                                 # سمك خط المفتاح ولإظهار السمك غيرها إلى legend_text_bold = "bold"
legend_color_option = True                              # لكي تأخذ المفاتيح لون الأسود غيرها إلى legend_color_option = False

#  تحديد أسماء الأعمدة 6   
dataset = dataset.rename(columns={

# غير الأسماء في الجهة اليسرى حسب الجدول الذي عندك   
    "PLAYER"            : "PLAYER",
    "METRIC"            : "METRIC",
    "RANK"              : "RANK",
    "CATEGORY"          : "CATEGORY",
    "COLOR"             : "COLOR",

})

#─────1. تجميع البيانات─────────────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

# تجهيز قائمة للاعبين بدون تكرار
selected_players = dataset["PLAYER"].unique()

if len(selected_players) > 0:

    # اختيار اللاعب الأول من القائمة
    player_name = selected_players[0]

    # تصفية البيانات للاعب المحدد
    player_data = dataset[dataset["PLAYER"] == player_name]

    # ترتيب البيانات حسب الصنف
    player_data = player_data.sort_values(by="CATEGORY")

    # تخزين البيانات في قوائم منفصلة
    metrics    = player_data["METRIC"].astype(str).tolist()    # ← قائمة أسماء الإحصائيات
    values     = player_data["RANK"].tolist()                  # ← قائمة قيم الترتيب
    colors     = player_data["COLOR"].astype(str).str.strip().tolist()     # ← قائمة الألوان
    categories = player_data["CATEGORY"].astype(str).tolist()  # ← قائمة الفئات

#─────2. تصميم الشكل────────────────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

    # حساب عدد الاحصائيات
    N = len(metrics)

    # حساب الزوايا لكل إحصائية
    angles = np.linspace(0, 2*np.pi, N+1)

    # رسم المخطط
    fig, ax = plt.subplots(figsize=(Width, Length), subplot_kw=dict(polar=True),dpi=600)

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
    ax.plot(theta, [100]*500, color="black", linewidth=0)         # ← خط الدائرة الخارجية

    # رسم الخطوط الفاصلة بين الإحصائيات
    for angle in angles[:-1]:
        ax.plot(
            [angle, angle],                          # ← اتجاه الخط (من الداخل للخارج)
            [Circle_size, 100 + Circle_size],    # ← نطاق الخط
            color=line_color,                        # ← لون الخط
            linestyle="-",                           # ← نوع الخط
            linewidth=1                              # ← سُمك الخط
        )

    # خلفية الشكل
    fig.patch.set_facecolor(background)              # ← لون خلفية الصورة

    # خلفية المحاور
    ax.set_facecolor(background)                     # ← لون خلفية المحاور

#─────3. رسم الأجزاء وكتابة القيم───────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

    # رسم الأجزاء الخارجية والداخلية لكل إحصائية
    for i in range(N):

        # حساب الزاوية لكل فئة
        start_angle = angles[i]
        end_angle   = angles[i+1]
        mid_angle   = (start_angle + end_angle) / 2

        # تحويل القيم إلى أرقام
        val =values[i]

        # تخزين لون الفئة
        base_color = colors[i]

        # رسم الجزء الخارجي (لون فاتح)
        ax.bar(
            mid_angle,                                        # ← زاوية المنتصف
            100,                                              # ← ارتفاع الشريط
            width=end_angle - start_angle,                    # ← عرض الشريط
            color=make_lighter(base_color, out_color_light),  # ← لون الجزء الخارجي (فاتح)
            edgecolor=line_color,                             # ← لون الفواصل
            bottom=Circle_size                              # ← بداية الشريط من الدائرة الداخلية
        )

        # حساب القيمة الفعلية بناءً على الترتيب
        new_val = ((Max_players - val + 1) / Max_players) * 100  # ← تحويل الترتيب إلى نسبة مئوية

        # رسم الجزء الداخلي (القيمة الفعلية)
        ax.bar(
            mid_angle,                         # ← زاوية المنتصف
            new_val,                           # ← ارتفاع الشريط (القيمة الفعلية)
            width=end_angle - start_angle,     # ← عرض الشريط
            color=base_color,                  # ← لون الفئة الأصلي
            edgecolor=line_color,              # ← لون الفواصل
            bottom=Circle_size               # ← بداية الشريط من الدائرة الداخلية
        )

        # كتابة القيمة داخل المخطط
        ax.text(
            mid_angle,                          # ← الموضع الأفقي (الزاوية)
            new_val + Circle_size,            # ← الموضع العمودي (فوق الشريط)
            f"{val:02.0f}",                     # ← النص المعروض (رقم الترتيب)
            ha="center",                        # ← محاذاة أفقية في المنتصف
            va="center",                        # ← محاذاة عمودية في المنتصف
            fontsize=Metric_Value_size,         # ← حجم الخط
            fontweight=Metric_Value_bold,       # ← سُمك الخط
            color=Metric_Value_color_text,      # ← لون النص
            bbox=dict(
                facecolor=make_lighter(base_color, Metric_Value_color_background_light),  # ← لون خلفية المربع
                edgecolor=Metric_Value_box_edgecolor,                                     # ← لون إطار المربع
                boxstyle=f"round,pad={Metric_Value_box_pad}"                              # ← شكل المربع
            )
        )

        # حساب زاوية دوران اسم الإحصائية
        rotation_angle = np.degrees(mid_angle) + 90
        if 0 < np.degrees(mid_angle) < 180:
            rotation_angle += 180                            # ← تصحيح اتجاه النص في النصف السفلي

        # تحديد لون اسم الإحصائية بناءً على الخيار المحدد
        if Metric_color_option == True:
            Metric_color = base_color                        # ← استخدام لون الفئة

        # كتابة اسم الإحصائية (مع معالجة النص العربي عبر ar())
        ax.text(
            mid_angle,                                       # ← الموضع الأفقي (الزاوية)
            Metric_distance + Circle_size,                 # ← الموضع العمودي (خارج المخطط)
            auto_split(metrics[i], max_len=12),          # ← النص (مع تقسيم تلقائي ومعالجة عربية)
            ha="center",                                     # ← محاذاة أفقية في المنتصف
            va="center",                                     # ← محاذاة عمودية في المنتصف
            fontsize=Metric_size,                            # ← حجم الخط
            fontweight=Metric_bold,                          # ← سُمك الخط
            rotation=rotation_angle,                         # ← زاوية دوران النص
            rotation_mode="anchor",                          # ← وضع الدوران
            color=Metric_color,                              # ← لون النص
        )

#─────4. العنوان والمفتاح───────────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

    # كتابة العنوان الرئيسي (مع معالجة النص العربي عبر ar())
    fig.text(
        0.515, 0.965,                  # ← موضع النص (أفقي، عمودي)
        First_tittel,              # ← نص العنوان
        size=First_tittel_size,        # ← حجم الخط
        ha="center",                   # ← محاذاة أفقية في المنتصف
        color=First_tittel_color,      # ← لون النص
        fontweight=First_tittel_bold,  # ← سُمك النص
    )

    # تجهيز قائمة الفئات والألوان لمفتاح المخطط
    categories = list(dict(zip(categories, colors)).items())

    # إنشاء عناصر المفتاح بناءً على الفئات والألوان (مع معالجة النص العربي عبر ar())
    legend_handles = [
        plt.Line2D([0], [0], color="none", label=label)  # ← عنصر مفتاح بدون خط
        for label, _ in categories
    ]

    # عرض المفتاح
    legend = fig.legend(
        handles=legend_handles,              # ← عناصر المفتاح
        loc='upper center',                  # ← موضع المفتاح
        bbox_to_anchor=(0.5, 0.96),          # ← إحداثيات المفتاح
        ncol=len(categories),                # ← عدد الأعمدة
        frameon=False,                       # ← إخفاء إطار المفتاح
        columnspacing=0,                     # ← المسافة بين الأعمدة
        fontsize=legend_text_size,           # ← حجم خط المفتاح
        prop={'size': legend_text_size, 'weight': legend_text_bold}  # ← حجم وسُمك الخط
    )

    # ضبط لون النص في المفتاح ليتناسب مع الألوان المستخدمة
    if legend_color_option:
        for text, (_, color) in zip(legend.get_texts(), categories):
            text.set_color(color)            # ← تطبيق لون الفئة على النص

#─────5. إظهار الرسم────────────────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────


fig.savefig('output_chart_hq.png', format='png', dpi=600,
            bbox_inches='tight', pad_inches=0,
            facecolor=fig.get_facecolor())

