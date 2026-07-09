# ⚡ DataOps & Workflow Automation Layer (`n8n Orchestration`) | طبقة الأتمتة وجدولة التشغيل

هذا المجلد (`n8n/`) مخصص لملفات وسير عمل الأتمتة (`Workflows`) الخاصة بمشروع التخرج باستخدام منصة **n8n Cloud / Self-Hosted**. يتيح هذا الملف للمقيّمين ولأعضاء فريق هندسة البيانات (`DataOps Engineer`) استيراد دورة التشغيل التلقائية وبث الإشعارات اللحظية على تليجرام بضغطة زر واحدة.

---

## 📂 محتويات المجلد (`Contents`)
- **`depi.json`**: ملف التصدير الرسمي للـ Workflow في n8n، ويحتوي على العقد (`Nodes`) التالية:
  1. **`Schedule Trigger` (الجدولة اليومية)**: تشغيل البايبلين يومياً عند منتصف الليل (`00:00 UTC`).
  2. **`SSH Node (Execute a command)`**: الاتصال الآمن بالسيرفر السحابي (`Hostinger Cloud VPS`) عبر الـ SSH وتشغيل حاوية استخراج بيانات الطقس:
     ```bash
     cd /root/depi_project && docker compose up -d --build weather-etl
     ```
  3. **`Telegram Notification Node`**: إرسال إشعار لحظي لحساب / جروب فريق العمل على تليجرام (`@wether_app_bot`) بنجاح سحب وتحميل بيانات 260 مدينة ومحافظة مصرية في قاعدة البيانات مع طابع زمني دقيق للتشغيل.

---

## ⚙️ كيفية استيراد وتشغيل الـ Workflow في منصة n8n (`Import Guide`)

إذا كنت تريد تجربة أو فحص هذا الـ Workflow داخل حسابك في n8n:

1. افتح لوحة التحكم الخاصة بك في **n8n** (سواء السحابية `n8n Cloud` أو المحلية).
2. اضغط على **`Add Workflow`** لإنشاء سير عمل جديد.
3. اضغط على القائمة العلوية يميناً (`...` أو `Workflow Settings`) ثم اختر **`Import from File`**.
4. حدد ملف **`depi.json`** الموجود في هذا المجلد (`depi_project/n8n/depi.json`).
5. ستظهر لك العقد الثلاث متصلة ببعضها: `Schedule Trigger` ➔ `Execute a command (SSH)` ➔ `Send a text message (Telegram)`.

---

## 🔑 إعدادات الصلاحيات والربط (`Credentials Setup`)

عند استيراد الملف، ستحتاج لربط الحسابات الخاصة بك ليعمل النظام بنجاح:
* **SSH Password account**: إدخال بيانات السيرفر السحابي (`Host IP: 72.62.92.93`, `User: root`, `Password`).
* **Telegram Bot Credentials**: إدخال الـ `Bot Token` الخاص ببوت التليجرام (`@wether_app_bot`) وتحديد الـ `Chat ID` التابع لك لاستقبال التنبيهات.

---

## 💬 نموذج الإشعار المستلم على تليجرام (`Telegram Alert Sample`)

عند انتهاء تنفيذ بايبلين الطقس بنجاح، يقوم n8n بإرسال هذه الرسالة الحية:
```text
✅ Weather ETL Pipeline Executed Successfully!
🌍 Extracted & Loaded 260 Egyptian cities into PostgreSQL.
⏰ Execution Time: 2026-07-09 16:18:29
```
