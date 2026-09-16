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
MEDIUM_RISK = [
    "كلب", "حمار", "غبي", "زفت", "ورع", "حقير", "تفه", "حيوان", "تيس", "قليل أدب"
]

HIGH_RISK = [
    "كس", "زُب", "زب", "طيز", "منيوك", "أنيك", "انيك", "شرموط", "قحبة", "قحبه", 
    "عرص", "قواد", "يا ابن الكلب", "يا ابن القحبة", "يلعن", "لعن",
    "تهديد", "اختراق", "ابتزاز", "احتيال", "مضايقة", "خطر", "صورة", "فضيحة", "بهكرك", "بفضحك"
]

# --- 3. المنطق ودوال المحادثة ---

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
        welcome_msg = f"مرحباً بك! تم تفعيل 🦊💖 **وضع الثعلب اللطيف للحماية** (العمر: {age} سنة)."
        return (
            gr.update(value=welcome_msg, visible=True),
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(visible=False)
        )
    else:
        welcome_msg = f"أهلاً بك! تم تفعيل ⚡ **الوضع المتقدم للشبكات والأمن السيبراني** (العمر: {age} سنة)."
        return (
            gr.update(value=welcome_msg, visible=True),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=True)
        )

# دالة الشات التفاعلي مع تغيير لون وحالة الثعلب اللطيف
def fox_chat_assistant(user_message, history):
    if not user_message or user_message.strip() == "":
        return "", history

    # 🔴 الحالة الحمراء: الثعلب يتحول للون الأحمر الغاضب والمنبه
    found_high = [word for word in HIGH_RISK if word in user_message]
    if found_high:
        censored = user_message
        for word in found_high:
            censored = re.sub(re.escape(word), "*" * len(word), censored)
        reply = (
            "🔴🔴🔴\n"
            "🦊😡 **الثعلب الأحمر الغاضب:**\n"
            "يا بطل! هذه الرسالة فيها خطر كبير وألفاظ محظورة جداً!\n\n"
            f"🛑 **النص المحجوب:** {censored}\n\n"
            "امسحها فوراً ولا ترد عليها، وأخبر والديك لحمايتك!"
        )
        history.append((user_message, reply))
        return "", history

    # 💛 الحالة الصفراء: الثعلب يتحول للون الأصفر الحذر والمفكر
    found_medium = [word for word in MEDIUM_RISK if word in user_message]
    if found_medium:
        censored = user_message
        for word in found_medium:
            censored = re.sub(re.escape(word), "*" * len(word), censored)
        reply = (
            "💛💛💛\n"
            "🦊ناو **الثعلب الأصفر المحذر:**\n"
            f"انتبه يا بطل! الرسالة فيها شتائم غير لائقة مثل ({', '.join(found_medium)}).\n\n"
            f"✨ **النص المعدل:** {censored}\n\n"
            "خلينا نكون دائماً لطيفين ونستخدم كلمات حلوة!"
        )
        history.append((user_message, reply))
        return "", history

    # 💙 الحالة الزرقاء/الوردية: الثعلب الكيوت السعيد واللطيف
    msg_lower = user_message.lower()
    if "رابط" in msg_lower or "غريب" in msg_lower:
        reply = "💙💙💙\n🦊✨ **الثعلب الأزرق الكيوت:**\nإذا وصلك رابط غريب لا تفتحه أبداً، استأذن بابا أو ماما أولاً يا بطل!"
    elif "كلمة سر" in msg_lower or "باسورد" in msg_lower:
        reply = "💙💙💙\n🦊🔐 **الثعلب الأزرق الكيوت:**\nكلمة السر سرية جداً! لا تشاركها مع أي أحد على النت إطلاقاً."
    elif "مرحبا" in msg_lower or "هلا" in msg_lower or "السلام" in msg_lower:
        reply = "💙💙💙\n🦊💖 **الثعلب اللطيف الكيوت:**\nأهلاً أهلاً يا بطل! أنا صديقك الثعلب الكيوت حارس الأمان. كيف أقدر أساعدك اليوم؟"
    else:
        reply = f"💙💙💙\n🦊🌟 **الثعلب الأزرق الكيوت:**\nرسالتك '{user_message}' آمنة ولطيفة جداً! أنا هنا دائماً عشان أحميك ونلعب بأمان."

    history.append((user_message, reply))
    return "", history

def predict_network(duration, bytes_sent):
    if duration is None or bytes_sent is None:
        return "⚠️ يرجى إدخال البيانات", "في انتظار المدخلات..."
    input_data = np.array([[duration, bytes_sent]])
    prediction = model.predict(input_data)[0]
    if prediction == -1:
        return "🔴 تنبيه أمني: هجوم / سلوك شاذ", "تم رصد حركة بيانات مشبوهة!"
    return "🔵 اتصال طبيعي وآمن", "الحركة سليمة ضمن المعدل الطبيعي."

# --- 4. الواجهة الرسومية ---

head_code = """
<meta name="description" content="نظام الحارس الذكي - Smart Guardian">
<title>نظام الحارس الذكي | Smart Guardian</title>
"""

with gr.Blocks(theme=gr.themes.Soft(), title="نظام الحارس الذكي | Smart Guardian", head=head_code) as app:
    
    gr.Markdown("# 🛡️ نظام الحارس الذكي (Smart Guardian)")
    status_banner = gr.Markdown("يرجى تسجيل الدخول للبدء", visible=True)
    
    # 1️⃣ تسجيل الدخول
    with gr.Column(visible=True) as login_box:
        gr.Markdown("### 🔑 تسجيل الدخول / إنشاء حساب")
        contact_in = gr.Textbox(label="البريد الإلكتروني أو رقم الهاتف", placeholder="example@email.com / 05xxxxxxxx")
        birth_in = gr.Textbox(label="تاريخ الميلاد (السنة-الشهر-اليوم)", value="2010-01-01", placeholder="YYYY-MM-DD")
        login_btn = gr.Button("دخول للنظام 🚀", variant="primary")

    # 2️⃣ واجهة الصغار (< 18 سنة): الثعلب اللطيف المتغير الألوان
    with gr.Column(visible=False) as junior_view:
        gr.Markdown("## 🦊💖 الثعلب اللطيف (يتغير شكله ولونه مع الرسائل)")
        gr.Markdown("تحدث مع الثعلب الكيوت: **💙 أزرق/وردي (آمن ولطيف)** | **💛 أصفر (محذر ومفكر)** | **🔴 أحمر (غاضب ومحظر)**")
        
        chatbot = gr.Chatbot(label="المحادثة مع الثعلب الكيوت 🦊✨", height=420)
        msg_input = gr.Textbox(placeholder="اكتب رسالتك للثعلب اللطيف هنا واضغط Enter...", label="رسالتك")
        send_btn = gr.Button("إرسال للثعلب 🚀", variant="primary")
        clear_btn = gr.Button("مسح المحادثة 🗑️")

        send_btn.click(fox_chat_assistant, inputs=[msg_input, chatbot], outputs=[msg_input, chatbot])
        msg_input.submit(fox_chat_assistant, inputs=[msg_input, chatbot], outputs=[msg_input, chatbot])
        clear_btn.click(lambda: None, None, chatbot, queue=False)

    # 3️⃣ واجهة الكبار (>= 18 سنة)
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

    login_btn.click(
        handle_login,
        inputs=[contact_in, birth_in],
        outputs=[status_banner, login_box, junior_view, senior_view]
    )

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=10000)
