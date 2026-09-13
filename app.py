import gradio as gr
import numpy as np
import re
from sklearn.ensemble import IsolationForest

# تدريب نموذج كشف الهجمات
X_train = np.array([
    [1, 300], [2, 450], [1, 350], [2, 400], [0, 310],
    [150, 5000000], [160, 6000000]
])
model = IsolationForest(contamination=0.2, random_state=42)
model.fit(X_train)

BLOCKED_WORDS = ["تهديد", "اختراق", "ابتزاز", "احتيال", "سب", "مضايقة"]

def predict_network(duration, bytes_sent):
    if duration is None or bytes_sent is None:
        return "⚠️ يرجى إدخال البيانات", "في انتظار المدخلات..."
    input_data = np.array([[duration, bytes_sent]])
    prediction = model.predict(input_data)[0]
    if prediction == -1:
        return "🔴 تنبيه أمني: هجوم / سلوك شاذ", "تم رصد حركة بيانات مشبوهة!"
    return "🔵 اتصال طبيعي وآمن", "الحركة سليمة ضمن المعدل الطبيعي."

def process_text_message(message):
    if not message or message.strip() == "":
        return "⚠️ النص فارغ", "", "يرجى كتابة نص"
    found_threats = [word for word in BLOCKED_WORDS if word in message]
    if found_threats:
        censored_text = message
        for word in found_threats:
            censored_text = re.sub(word, "*" * len(word), censored_text)
        return "🔴 تنبيه أمني: محتوى مسيء", censored_text, "تم حجب الكلمات وإرسال إشعار"
    return "🔵 رسالة آمنة", message, "عرض النص بشكل طبيعي"

with gr.Blocks(theme=gr.themes.Soft(), title="نظام الحارس الذكي") as app:
    gr.Markdown("# 🛡️ نظام الحارس الذكي للأمن السايبري")
    with gr.Tabs():
        with gr.TabItem("🌐 كشف هجمات الشبكة"):
            duration_in = gr.Number(label="مدة الاتصال", value=2)
            bytes_in = gr.Number(label="حجم البيانات", value=500)
            btn_net = gr.Button("🔍 فحص", variant="primary")
            net_res_status = gr.Textbox(label="حالة الاتصال", interactive=False)
            net_res_act = gr.Textbox(label="القرار", interactive=False)
            btn_net.click(predict_network, inputs=[duration_in, bytes_in], outputs=[net_res_status, net_res_act])

        with gr.TabItem("💬 حماية المحادثات"):
            text_in = gr.Textbox(lines=3, label="الرسالة")
            btn_text = gr.Button("🛡️ فحص", variant="primary")
            text_res_status = gr.Textbox(label="النتيجة", interactive=False)
            text_res_censored = gr.Textbox(label="الرسالة المعالجة", interactive=False)
            text_res_act = gr.Textbox(label="الإجراء", interactive=False)
            btn_text.click(process_text_message, inputs=[text_in], outputs=[text_res_status, text_res_censored, text_res_act])

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=10000)
