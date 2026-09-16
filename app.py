import gradio as gr
import numpy as np
import re
from datetime import datetime
from sklearn.ensemble import IsolationForest

# --- 1. إعداد نموذج الذكاء الاصطناعي للشبكة ---
X_train = np.array([
    [1, 300], [2, 450], [1, 350], [2, 400], [0, 310],
    [150, 5000000], [160, 6000000]
])
model = IsolationForest(contamination=0.2, random_state=42)
model.fit(X_train)

# --- 2. تصنيف الكلمات وحظر السباب والقذف ---

# المستوى الأصفر: شتائم خفيفة وكلمات يومية
MEDIUM_RISK = [
    "كلب", "حمار", "غبي", "زفت", "ورع", "حقير", "تفه", "حيوان", "تيس", "قليل أدب"
]

# المستوى الأحمر: قذف مباشر، ألفاظ نابية شديدة، تهديد، واختراق
HIGH_RISK = [
    # ألفاظ نابية وقذف صريح
    "كس", "زُب", "زب", "طيز", "منيوك", "أنيك", "انيك", "شرموط", "قحبة", "قحبه", 
    "عرص", "قواد", "يا ابن الكلب", "يا ابن القحبة", "يلعن", "لعن",
    
    # تهديدات وابتزاز وأمن سيبراني
    "تهديد", "اختراق", "ابتزاز", "احتيال", "مضايقة", "خطر", "صورة", "فضيحة", "بهكرك", "بفضحك"
]

# --- 3. دوال معالجة المنطق والتسجيل ---

def calculate_age(birth_date_str):
    if not birth_date_str:
        return 18
    try:
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
        today = datetime.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    except ValueError:
        return 18

def handle_login(contact_info, birth_date_str):
    if not contact_info or contact_info.strip() == "":
        return (
            gr.update(value="⚠️ يرجى كتابة البريد أو رقم الهاتف أولاً.", visible=True),
            gr.update(visible=True),
            gr.update(visible=False),
            gr.update(visible=False)
        )
    
    age = calculate_age(birth_date_str)
    
    if age < 18:
        welcome_msg = f"مرحباً بك! تم تفعيل 🦊 **وضع الثعلب الذكي وحماية الصغار** (العمر: {age} سنة)."
        return (
            gr.update(value=welcome_msg, visible=True),
            gr.update(visible=False), # إخفاء شاشة التسجيل
            gr.update(visible=True),  # إظهار واجهة الثعلب للصغار
            gr.update(visible=False)  # إخفاء المتقدم
        )
    else:
        welcome_msg = f"أهلاً بك! تم تفعيل ⚡ **الوضع المتقدم للشبكات والأمن السيبراني** (العمر: {age} سنة)."
        return (
            gr.update(value=welcome_msg, visible=True),
            gr.update(visible=False), # إخفاء شاشة التسجيل
            gr.update(visible=False), # إخفاء واجهة الصغار
            gr.update(visible=True)   # إظهار المتقدم
        )

def fox_smart_checker(message):
    if not message or message.strip() == "":
        return (
            "🦊 **الثعلب الذكي:** اكتب لي أي رسالة لنفحصها معاً!",
            "💙 مستوى الأمان: منتظر",
            "أهلاً بك يا بطل!"
        )
    
    # 1. فحص المستوى الأحمر (ألفاظ نابية شديدة / قذف / تهديد)
    found_high = [word for word in HIGH_RISK if word in message]
    if found_high:
        censored = message
        for word in found_high:
            censored = re.sub(re.escape(word), "*" * len(word), censored)
        return (
            f"🔴 **خطر شديد! (ألفاظ محظورة / قذف)**\n\n🦊 **الثعلب يصرخ:** تم رصد كلمات نابية أو خطيرة جداً! تم حجبها فوراً.\nيرجى الالتزام بالآداب العامة وعدم تداول هذه الألفاظ.",
            "🔴 خطر أحمر - محتوى محظور شديد",
            f"النص المعالج: {censored}"
        )
    
    # 2. فحص المستوى الأصفر (سب خفيف / شتائم عادية)
    found_medium = [word for word in MEDIUM_RISK if word in message]
    if found_medium:
        censored = message
        for word in found_medium:
            censored = re.sub(re.escape(word), "*" * len(word), censored)
        return (
            f"💛 **تحذير (سب غير لائق)**\n\n🦊 **الثعلب يفكر:** انتبه يا بطل! الرسالة فيها شتائم مثل ({', '.join(found_medium)}).\nيفضل استخدام كلمات أرقى في الحديث.",
            "💛 تحذير أصفر - تنبيه على الألفاظ",
            f"النص المعالج: {censored}"
        )
    
    # 3. المستوى الأزرق (آمن)
    return (
        "💙 **رسالة آمنة ولائقة تماماً!**\n\n🦊 **الثعلب يبتسم:** ممتاز! هذه الرسالة آمنة وخالية من الشتائم.",
        "💙 أمان أزرق - حالة سليمة",
        f"النص: {message}"
    )

def predict_network(duration, bytes_sent):
    if duration is None or bytes_sent is None:
        return "⚠️ يرجى إدخال البيانات", "في انتظار المدخلات..."
    input_data = np.array([[duration, bytes_sent]])
    prediction = model.predict(input_data)[0]
    if prediction == -1:
        return "🔴 تنبيه أمني: هجوم / سلوك شاذ", "تم رصد حركة بيانات مشبوهة!"
    return "🔵 اتصال طبيعي وآمن", "الحركة سليمة ضمن المعدل الطبيعي."

# --- 4. بناء الواجهة الرسومية ---

head_code = """
<meta name="description" content="نظام الحارس الذكي - Smart Guardian: تطبيق أمن سيبراني متكامل وحماية من السباب والقذف.">
<title>نظام الحارس الذكي | Smart Guardian</title>
"""

with gr.Blocks(theme=gr.themes.Soft(), title="نظام الحارس الذكي | Smart Guardian", head=head_code) as app:
    
    gr.Markdown("# 🛡️ نظام الحارس الذكي (Smart Guardian)")
    status_banner = gr.Markdown("يرجى تسجيل الدخول للبدء", visible=True)
    
    # 1️⃣ شاشة تسجيل الدخول
    with gr.Column(visible=True) as login_box:
        gr.Markdown("### 🔑 تسجيل الدخول / إنشاء حساب")
        contact_in = gr.Textbox(label="البريد الإلكتروني أو رقم الهاتف", placeholder="example@email.com / 05xxxxxxxx")
        birth_in = gr.Textbox(label="تاريخ الميلاد (السنة-الشهر-اليوم)", value="2010-01-01", placeholder="YYYY-MM-DD")
        login_btn = gr.Button("دخول للنظام 🚀", variant="primary")

    # 2️⃣ واجهة الناشئين والصغار (< 18 سنة)
    with gr.Column(visible=False) as junior_view:
        gr.Markdown("## 🦊 وضع الثعلب الذكي وحماية الصغار")
        gr.Markdown("نظام الألوان: **💙 أزرق (آمن)** | **💛 أصفر (تحذير/سب خفيف)** | **🔴 أحمر (قذف/خطر شديد)**")
        
        child_input = gr.Textbox(lines=2, label="اكتب أو ألصق الرسالة هنا يا بطل:", placeholder="اكتب الرسالة هنا...")
        check_btn = gr.Button("🔍 افحص مع الثعلب", variant="primary")
        
        fox_reply = gr.Markdown("🦊 الثعلب ينتظر رسالتك...")
        alert_color = gr.Textbox(label="مستوى الخطر واللون", interactive=False)
        processed_text = gr.Textbox(label="معالجة النص وحجب الكلمات", interactive=False)
        
        check_btn.click(
            fox_smart_checker,
            inputs=[child_input],
            outputs=[fox_reply, alert_color, processed_text]
        )

    # 3️⃣ واجهة المتقدمين للكبار (>= 18 سنة)
    with gr.Column(visible=False) as senior_view:
        gr.Markdown("## ⚡ أدوات الأمن السيبراني المتقدمة")
        with gr.Tabs():
            with gr.TabItem("🌐 كشف هجمات الشبكة"):
                duration_in = gr.Number(label="مدة الاتصال (ثواني)", value=2)
                bytes_in = gr.Number(label="حجم البيانات (Bytes)", value=500)
                btn_net = gr.Button("🔍 فحص الاتصال", variant="primary")
                net_res_status = gr.Textbox(label="حالة الاتصال", interactive=False)
                net_res_act = gr.Textbox(label="القرار والجراء", interactive=False)
                btn_net.click(predict_network, inputs=[duration_in, bytes_in], outputs=[net_res_status, net_res_act])

            with gr.TabItem("🦊 فحص النصوص مع الثعلب"):
                sr_input = gr.Textbox(lines=2, label="فحص الرسائل أو المحتوى:")
                sr_btn = gr.Button("🔍 فحص", variant="primary")
                sr_fox_reply = gr.Markdown()
                sr_alert_color = gr.Textbox(label="مستوى الخطر", interactive=False)
                sr_processed_text = gr.Textbox(label="النص المعالج", interactive=False)
                sr_btn.click(fox_smart_checker, inputs=[sr_input], outputs=[sr_fox_reply, sr_alert_color, sr_processed_text])

    # ربط زر التسجيل
    login_btn.click(
        handle_login,
        inputs=[contact_in, birth_in],
        outputs=[status_banner, login_box, junior_view, senior_view]
    )

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=10000)
