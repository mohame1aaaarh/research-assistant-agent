# 🤖 Research Assistant Agent | مساعد البحث الذكي

![Research Assistant Banner](research_assistant_banner_1778159652862.png)

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/mohame1aaaarh/research-assistant-agent)
[![Python Version](https://img.shields.io/badge/Python-3.9+-green?logo=python)](https://www.python.org/)
[![Chainlit](https://img.shields.io/badge/UI-Chainlit-orange)](https://chainlit.io/)
[![Agno](https://img.shields.io/badge/Framework-Agno-purple)](https://agno.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Overview | نظرة عامة

**English:**
The **Research Assistant Agent** is a sophisticated AI-powered tool designed for researchers and students. It streamlines the academic workflow by searching global databases, analyzing PDF documents, and providing expert-level summaries with full citations. Built with a focus on accuracy and scholarly integrity.

**العربية:**
**مساعد البحث الذكي** هو أداة متطورة تعتمد على الذكاء الاصطناعي مصممة خصيصاً للباحثين والطلاب. يهدف المشروع إلى تسهيل العمل الأكاديمي من خلال البحث في قواعد البيانات العالمية، تحليل ملفات PDF، وتقديم ملخصات دقيقة مع توثيق كامل للمصادر. تم بناء النظام مع التركيز على الدقة والأمانة العلمية.

---

## ✨ Key Features | المميزات الرئيسية

| Feature | الميزة | Description | الوصف |
| :--- | :--- | :--- | :--- |
| 🔍 **Academic Search** | **البحث الأكاديمي** | Integration with **ArXiv** for the latest papers. | الوصول الفوري لأحدث الأبحاث عبر **ArXiv**. |
| 📄 **PDF Analysis** | **تحليل الملفات** | Extract insights and data from uploaded PDF files. | استخراج البيانات والرؤى من ملفات PDF المرفقة. |
| 🌐 **Web Research** | **البحث عبر الويب** | Real-time search using **DuckDuckGo** and **Wikipedia**. | بحث فوري وشامل باستخدام محركات البحث العالمية. |
| 📍 **Smart Citations** | **توثيق ذكي** | Automatic **APA** citation generation for all sources. | توثيق تلقائي للمصادر بنظام **APA** لضمان الموثوقية. |
| 💬 **Bilingual Support** | **دعم ثنائي اللغة** | Full support for Arabic and English interaction. | دعم كامل للتفاعل باللغتين العربية والإنجليزية. |

---

## 🛠️ Tech Stack | التقنيات المستخدمة

- **Frontend:** [Chainlit](https://github.com/Chainlit/chainlit) (Real-time Conversational UI)
- **Agent Framework:** [Agno](https://github.com/agno-ai/agno) (formerly Phidata)
- **LLM Provider:** [OpenRouter](https://openrouter.ai/) (Access to Llama 3.1 & GPT-4o)
- **Memory/Database:** [SQLite](https://www.sqlite.org/) (Session & History persistence)
- **Tools:** ArXiv, Wikipedia, DuckDuckGo, PyPDF.

---

## 🚀 Getting Started | كيف تبدأ

### 1️⃣ Clone the Repository | نسخ المشروع
```bash
git clone https://github.com/mohame1aaaarh/research-assistant-agent.git
cd research-assistant-agent
```

### 2️⃣ Install Dependencies | تثبيت المكتبات
It is recommended to use a virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
pip install -r requirements.txt
```

### 3️⃣ Configuration | الإعدادات
Create a `config.py` file or set up your environment variables:
```python
# config.py
OPENROUTER_KEY = "your_openrouter_api_key_here"
```

### 4️⃣ Run the Application | تشغيل التطبيق
```bash
chainlit run app.py
```

---

## 📂 Project Structure | هيكل المشروع

```text
research-assistant-agent/
├── app.py             # Main Chainlit application
├── agent.py           # Agno agent configuration
├── config.py          # Configuration & API Keys
├── tools/             # Custom research & citation tools
├── database/          # Auth & Memory logic (SQLite)
├── public/            # Static assets
└── requirements.txt   # Project dependencies
```

---

## 🤝 Contributing | المساهمة

We welcome contributions! If you have ideas for new features or improvements, feel free to open an issue or submit a pull request.

نرحب بجميع المساهمات! إذا كان لديك أفكار لميزات جديدة أو تحسينات، لا تتردد في فتح "Issue" أو إرسال "Pull Request".

---

## 📜 License | الترخيص

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### 👨‍💻 Developed by [Logic Lords](https://github.com/mohame1aaaarh)
*Made with ❤️ for the research community.*
