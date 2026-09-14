import pandas as pd
import matplotlib.pyplot as plt


# الاعتماد على خط عربي متوفر في النظام (بدون ملف خط خارجي)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Calibri', 'Tahoma', 'Segoe UI', 'Arial']
plt.rcParams['axes.unicode_minus'] = False
font_prop = None

#─────0. تحديد القيم────────────────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────
# ألوان الفريقين
Color_A = "#4D8C48"
Color_B = "#862424"
# خاص بالعنوان الرئيسي 1
First_tittel         = "إحصائيات الفريقين"            # ← نص العنوان الرئيسي
First_tittel_color   = "#9B30D0"                 # ← لون العنوان الرئيسي
First_tittel_size    = 15                        # ← حجم العنوان الرئيسي
First_tittel_bold    = "bold"                    # ← سمك العنوان الرئيسي | None لإزالة السمك

# خاص بأسماء الفريقين في الترويسة 2
Team_title_size    = 17                        # ← حجم خط أسماء الفريقين
Team_title_bold    = "bold"                    # ← سمك خط أسماء الفريقين | None لإزالة السمك

# خاص بألوان الأرقام 3
Value_color        = "#111111"                 # ← لون الأرقام على يميني ويسار الأشرطة
Value_size         = 11                        # ← حجم خط الأرقام
Value_bold         = "bold"                    # ← سمك خط الأرقام | None لإزالة السمك

# خاص بتسميات المقاييس 4
Metric_label_color = "#555555"                 # ← لون اسم المقياس فوق كل شريط
Metric_label_size  = 13                       # ← حجم خط اسم المقياس

# خاص بأبعاد الأشرطة والشكل 5
Bar_height         = 0.4                      # ← ارتفاع كل شريط (القيم بين 0.1 و 0.6)
Row_height         = 0.55                      # ← ارتفاع كل صف (يتحكم في المسافة بين الأشرطة)
Fig_width          = 8                        # ← عرض الشكل بالبوصة

# خاص بالخلفية 6
BG_color           = "#FFFFFF"                 # ← لون خلفية الشكل كاملاً
Margin_left        = 0.20                      # ← هامش يسار الشريط (القيم بين 0 و 1)
Margin_right       = 0.20                      # ← هامش يمين الشريط (القيم بين 0 و 1)

#  تحديد أسماء الأعمدة 6
dataset = dataset.rename(columns={

# غير الأسماء في الجهة اليسرى حسب الجدول الذي عندك   
    "TEAM"             : "TEAM",
    "METRIC"                 : "METRIC",
    "VALUE"                 : "VALUE",

})

#─────1. تجميع البيانات─────────────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────

# استخراج الفرق بدون تكرار
selected_team = dataset["TEAM"].unique()

if len(selected_team) >= 2:

    # اختيار الفريق الأول والثاني من القائمة
    Team_A_name = selected_team[0]
    Team_B_name = selected_team[1]

    # تخزين بيانات الفريق الأول و الثاني 
    Team_A_data   = dataset[dataset["TEAM"] == Team_A_name]
    Team_B_data   = dataset[dataset["TEAM"] == Team_B_name]   

    Team_A_value = Team_A_data["VALUE"].astype(float).tolist()          # ← قيم اللاعب الأول
    Team_B_value = Team_B_data["VALUE"].astype(float).tolist()          # ← قيم اللاعب الثاني

    metrics  = Team_A_data["METRIC"].astype(str).tolist()          # ← قائمة أسماء الإحصائيات

    len_metrics = len(metrics)                                          # ← عدد الصفوف (المقاييس)

    pct_metrics = [m for m in metrics if "%" in m]      # ← المقاييس التي تعرض علامة % مع رقمها

    Fig_H  = len_metrics * Row_height + 2                                  # ← ارتفاع الشكل يُحسب تلقائياً حسب عدد الصفوف

    rows = []
    for i in range(len_metrics):
        rows.append({
        "Metric": metrics[i],
        'Team_A_V':  Team_A_value[i], 
        'Team_B_V':  Team_B_value[i], 
        'total': Team_A_value[i]+ Team_B_value[i],     
        'Team_A':  Team_A_value[i] / (Team_A_value[i]+ Team_B_value[i]),         
        'Team_B': Team_B_value[i] / (Team_A_value[i]+ Team_B_value[i])
        })

    data = pd.DataFrame(rows)

#─────2. تصميم الشكل────────────────────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(Fig_width, Fig_H))   # ← إنشاء لوحة الرسم بالأبعاد المحددة
    fig.patch.set_facecolor(BG_color)                    # ← تحديد لون خلفية الشكل الخارجية
    ax.set_facecolor(BG_color)                           # ← تحديد لون خلفية منطقة الرسم الداخلية

#─────3. رسم الأجزاء وكتابة القيم───────────────────────────────────────────────────────
#────────────────────────────────────────────────────────────────────────────────────────
    for i, row in data.iterrows():
                
        y = len_metrics - 1 - i                                    # ← نعكس الترتيب لتظهر الأشرطة من الأعلى للأسفل
        # ── شريط الفريق A ─────────────────────────────────────────────────────────
        ax.barh(y, row['Team_A'],                        # ← طول الشريط = نسبة الفريق A
        left=0,                                  # ← يبدأ من أقصى اليسار
        height=Bar_height,                       # ← ارتفاع الشريط
        color=Color_A,                           # ← لون الشريط
        align='center',                          # ← محاذاة الشريط على المحور Y
        zorder=2)                                # ← طبقة الرسم (فوق الخلفية)

        # ── شريط الفريق B ─────────────────────────────────────────────────────────
        ax.barh(y, row['Team_B'],                        # ← طول الشريط = نسبة الفريق B
        left=row['Team_A'],                      # ← يبدأ من حيث انتهى شريط A
        height=Bar_height,                       # ← ارتفاع الشريط
        color=Color_B,                           # ← لون الشريط
        align='center',                          # ← محاذاة الشريط على المحور Y
        zorder=2)                                # ← طبقة الرسم (فوق الخلفية)
        
    # ── اسم المقياس فوق الشريط ───────────────────────────────────────────────
        ax.text(0.5,                                     # ← موضع النص أفقياً (المنتصف)
                y + Bar_height / 2 + 0.09,              # ← موضع النص عمودياً (فوق الشريط مباشرة)
                row['Metric'],                           # ← نص اسم المقياس
                ha='center',                             # ← محاذاة أفقية في المنتصف
                va='bottom',                             # ← محاذاة عمودية من الأسفل
                fontsize=Metric_label_size,              # ← حجم الخط
                color=Metric_label_color,                # ← لون النص
                fontproperties=font_prop,                # ← نوع الخط
                zorder=5)                                # ← طبقة الرسم (في الأمام)

        # ── قيمة الفريق A على اليسار ─────────────────────────────────────────────
        val_a   = row['Team_A_V']
        label_a = f"{val_a:.2f}%" if row['Metric'] in pct_metrics else str(int(val_a))   # ← إضافة % للمقاييس النسبية
        ax.text(-0.02, y,                                # ← موضع الرقم خارج الشريط يساراً
                label_a,                                 # ← نص الرقم
                ha='right',                              # ← محاذاة من اليمين
                va='center',                             # ← محاذاة عمودية في المنتصف
                fontsize=Value_size,                     # ← حجم الخط
                fontweight=Value_bold,                   # ← سمك الخط
                color=Value_color,                       # ← لون الرقم
                fontproperties=font_prop,                # ← نوع الخط
                zorder=5)                                # ← طبقة الرسم (في الأمام)

        # ── قيمة الفريق B على اليمين ─────────────────────────────────────────────
        val_b   = row['Team_B_V']
        label_b = f"{val_b:.2f}%" if row['Metric'] in pct_metrics else str(int(val_b))   # ← إضافة % للمقاييس النسبية
        ax.text(1.02, y,                                 # ← موضع الرقم خارج الشريط يميناً
                label_b,                                 # ← نص الرقم
                ha='left',                               # ← محاذاة من اليسار
                va='center',                             # ← محاذاة عمودية في المنتصف
                fontsize=Value_size,                     # ← حجم الخط
                fontweight=Value_bold,                   # ← سمك الخط
                color=Value_color,                       # ← لون الرقم
                fontproperties=font_prop,                # ← نوع الخط
                zorder=5)                                # ← طبقة الرسم (في الأمام)
                                    
    # ══════════════════════════════════════════════════════════════════════════════
    #  5. الترويسة (أسماء الفريقين + العنوان الرئيسي)
    # ══════════════════════════════════════════════════════════════════════════════

    header_y = len_metrics - 0.20                                  # ← الموضع العمودي للترويسة (فوق آخر شريط)

    # كتابة اسم الفريق A
    ax.text(0.18, header_y,                              # ← موضع الاسم (يسار)
            Team_A_name,                                 # ← نص الاسم
            ha='center',                                 # ← محاذاة أفقية في المنتصف
            va='bottom',                                 # ← محاذاة عمودية من الأسفل
            fontsize=Team_title_size,                    # ← حجم الخط
            fontweight=Team_title_bold,                  # ← سمك الخط
            color=Color_A,                     # ← لون الاسم
            fontproperties=font_prop,                    # ← نوع الخط
            transform=ax.transData)                      # ← إحداثيات بيانات المحور

    # كتابة اسم الفريق B
    ax.text(0.82, header_y,                              # ← موضع الاسم (يمين)
            Team_B_name,                                 # ← نص الاسم
            ha='center',                                 # ← محاذاة أفقية في المنتصف
            va='bottom',                                 # ← محاذاة عمودية من الأسفل
            fontsize=Team_title_size,                    # ← حجم الخط
            fontweight=Team_title_bold,                  # ← سمك الخط
            color=Color_B,                     # ← لون الاسم
            fontproperties=font_prop,                    # ← نوع الخط
            transform=ax.transData)                      # ← إحداثيات بيانات المحور

    # كتابة العنوان الرئيسي GAME SUMMARY
    ax.text(0.5, header_y + 0.60,                        # ← موضع العنوان (الوسط، أعلى من الأسماء)
            First_tittel,                                  # ← نص العنوان
            ha='center',                                 # ← محاذاة أفقية في المنتصف
            va='bottom',                                 # ← محاذاة عمودية من الأسفل
            fontsize=First_tittel_size,                    # ← حجم الخط
            fontweight=First_tittel_bold,                  # ← سمك الخط
            color=First_tittel_color,                      # ← لون العنوان
            fontproperties=font_prop,                    # ← نوع الخط
            transform=ax.transData)                      # ← إحداثيات بيانات المحور

    # ══════════════════════════════════════════════════════════════════════════════
    #  6. إعدادات المحاور والحفظ
    # ══════════════════════════════════════════════════════════════════════════════

    ax.set_xlim(-Margin_left, 1 + Margin_right)          # ← تحديد نطاق المحور الأفقي مع الهوامش
    ax.set_ylim(-0.55, len_metrics + 0.90)                         # ← تحديد نطاق المحور العمودي
    ax.axis('off')                                       # ← إخفاء المحاور والإطار

    fig.savefig('output_chart_hq.png', format='png', dpi=600,
                bbox_inches='tight', pad_inches=0.1,
                facecolor=fig.get_facecolor())            # ← حفظ الشكل بجودة عالية (600 dpi)

    plt.tight_layout(pad=0.5)                            # ← ضبط المسافات الداخلية تلقائياً
    plt.show()                                           # ← عرض الرسم النهائي على الشاشة