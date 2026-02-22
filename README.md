# 🤖 Research Assistant Agent
### مشروع التخرج — فريق التطوير

---

> **كلمة من قائد الفريق:**
> الملف ده هو مرجعنا الأساسي طول فترة المشروع.
> كل حاجة محتاج تعرفها عن المشروع، الأدوات، وخطة الشغل موجودة هنا.
> اقراه كويس، وأي سؤال — أنا موجود.

---

## 📋 فهرس المحتويات

1. [فكرة المشروع](#-فكرة-المشروع)
2. [الأدوات اللي هنشتغل بيها](#-الأدوات)
3. [هيكل المشروع](#-هيكل-المشروع)
4. [خطة التنفيذ والمحطات](#-خطة-التنفيذ)
5. [أدوار الفريق](#-أدوار-الفريق)
6. [قواعد الشغل مع بعض](#-قواعد-الشغل)

---

## 💡 فكرة المشروع

### المشكلة
الباحث والطالب بيضيع ساعات طويلة في البحث اليدوي عبر عشرات الأوراق البحثية، ومش قادر يحصل على إجابة سريعة وموثوقة مع مصدرها.

### الحل
نظام ذكاء اصطناعي يعمل كـ **مساعد بحث شخصي** — بيبحث في المصادر الأكاديمية، بيقرأ ملفات PDF، بيلخص الأوراق البحثية، وبيجاوب على أي سؤال مع ذكر المصدر تلقائياً — بالعربي والإنجليزي.

### اللي المشروع هيعمله

| الخاصية | الوصف |
|---|---|
| ✅ البحث الأكاديمي التلقائي | بيبحث في ArXiv و Semantic Scholar و DuckDuckGo |
| ✅ رفع PDF | بيقرأ أي ورقة بحثية ترفعها ويجاوب عليها |
| ✅ Citations أوتوماتيك | كل إجابة فيها مصدرها ومكانها بالظبط |
| ✅ تلخيص الأوراق | ملخص سريع لأي ورقة في ثواني |
| ✅ تاريخ المحادثات | بيحفظ كل أسئلتك وترجعلها أي وقت |
| ✅ عربي وإنجليزي | بيفهم ويرد بالاتنين |

---

## 🛠 الأدوات

### كيف بتتكلم الأدوات مع بعض

```
المستخدم
    ↓
Chainlit  ← (الواجهة — اللي المستخدم بيشوفه)
    ↓
Agno Agent  ← (المخ — بيقرر هيعمل إيه)
    ↓
┌───────────────────────────────┐
│  ArXiv  │  DuckDuckGo  │ PDF  │  ← (الأدوات — بتجيب المعلومات)
└───────────────────────────────┘
    ↓
Gemini Flash  ← (الذكاء — بيفهم ويكتب الإجابة)
    ↓
SQLite  ← (الذاكرة — بيحفظ المحادثات)
    ↓
المستخدم بيشوف الإجابة مع المصادر
```

---

### 1. 🎨 Chainlit — الواجهة

**بتعمل إيه:**
هي اللي المستخدم بيشوفها ويتعامل معاها. بتعمل Chat Interface شبه ChatGPT بالظبط، فيها عرض المصادر والـ Citations وتاريخ المحادثات — كل ده built-in من غير ما نكتبه.

**ليه اخترناها:**
لأنها مصممة أصلاً لـ AI Chat Apps، وبتتكتب بـ Python خالص، وشكلها احترافي من أول يوم.

**مثال بسيط:**
```python
import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    # لما المستخدم يبعت رسالة، هنا بنرد عليه
    await cl.Message(
        content=f"استلمت سؤالك: {message.content}"
    ).send()
```

---

### 2. 🧠 Agno — المخ والـ Agent

**بتعمل إيه:**
هو اللي بيقرر إزاي يرد على السؤال. بيحلل السؤال، بيقرر هيبحث فين، بيجمع النتائج، وبيبعتها لـ Gemini يلخصها. من غيره كنا هنكتب كل الخطوات دي بإيدينا.

**ليه اخترناها:**
أسهل framework موجود للـ AI Agents. الكود فيها واضح وقريب من Python العادي اللي إحنا عارفينه.

**مثال بسيط:**
```python
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[DuckDuckGoTools()],
    instructions="أنت مساعد بحث أكاديمي متخصص"
)

agent.print_response("إيه أحدث أبحاث الـ Neural Networks؟")
```

---

### 3. ✨ Gemini Flash — الذكاء الاصطناعي

**بتعمل إيه:**
هو اللي بيفهم اللغة فعلاً ويكتب الإجابات. Agno بيبعتله السؤال والمعلومات اللي جمعها، وGemini بيحولهم لإجابة مفهومة ومنظمة.

**ليه اخترناه:**
مجاني بـ Free Tier كافي جداً لمشروع كلية، وبيدعم العربي كويس، وأسرع من غيره.

**مثال بسيط:**
```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-2.0-flash-exp")

response = model.generate_content("لخصلي ورقة بحثية عن الـ AI")
print(response.text)
```

---

### 4. 🔍 ArXiv API — بحث الأوراق العلمية

**بتعمل إيه:**
بتدينا وصول مباشر لأكبر قاعدة أوراق بحثية في العالم — فيزياء، رياضيات، علوم حاسب، وأكتر. مجانية 100% ومن غير API Key.

**ليه اخترناها:**
متخصصة في الأبحاث العلمية بالظبط اللي مشروعنا محتاجه، ومجانية تماماً وبدون حدود.

**مثال بسيط:**
```python
import arxiv

client = arxiv.Client()
search = arxiv.Search(
    query="neural networks 2024",
    max_results=5
)

for paper in client.results(search):
    print(paper.title)
    print(paper.summary)
    print(paper.pdf_url)
```

---

### 5. 🌐 DuckDuckGo Search — البحث العام

**بتعمل إيه:**
بتدي الـ Agent قدرة يبحث في الإنترنت للأسئلة العامة اللي مش أكاديمية خالص. مجانية وما تحتاجش API Key خالص.

**ليه اخترناها:**
مجانية 100%، مفيش تسجيل، ومباشرة في Agno كـ built-in tool.

**مثال بسيط:**
```python
from agno.tools.duckduckgo import DuckDuckGoTools

# بيتضاف كـ tool للـ Agent مباشرة
tools = [DuckDuckGoTools()]
# الـ Agent هيستخدمه أوتوماتيك لما يحتاج يبحث
```

---

### 6. 📄 PDF Reader — قراءة الملفات

**بتعمل إيه:**
بتقرأ أي PDF يرفعه المستخدم، بتقطعه لأجزاء صغيرة، وبتبعتها للـ Agent يفهمها ويجاوب عليها.

**ليه اخترناها:**
Agno فيها PDF tool جاهزة built-in، ومش محتاجين نكتب كود إضافي.

**مثال بسيط:**
```python
from agno.agent import Agent
from agno.tools.file import FileTools

agent = Agent(
    tools=[FileTools()],
    instructions="اقرأ الملف وأجب على الأسئلة منه"
)

agent.print_response("لخصلي الملف ده", files=["paper.pdf"])
```

---

### 7. 🗄️ SQLite — الذاكرة

**بتعمل إيه:**
بتحفظ تاريخ المحادثات عشان لما المستخدم يرجع يلاقي كل أسئلته وإجاباته القديمة. مدمجة في Python من غير أي إعداد.

**ليه اخترناها:**
مدمجة في Python خالص — مش محتاجين نثبت أي حاجة، وكافية تماماً لمشروع كلية.

**مثال بسيط:**
```python
import sqlite3

conn = sqlite3.connect("conversations.db")
cursor = conn.cursor()

# حفظ محادثة
cursor.execute(
    "INSERT INTO history (question, answer) VALUES (?, ?)",
    ("إيه الـ AI؟", "الذكاء الاصطناعي هو...")
)
conn.commit()
```

---

## 📁 هيكل المشروع

```
research-assistant/
│
├── 📄 app.py                  ← نقطة البداية — شغّل ده وهيشتغل كل حاجة
├── 🧠 agent.py                ← الـ Agent الرئيسي (Agno)
├── 🔍 tools/
│   ├── search_tool.py         ← أدوات البحث (ArXiv + DuckDuckGo)
│   ├── pdf_tool.py            ← قراءة وتحليل PDF
│   └── citation_tool.py      ← توليد المصادر أوتوماتيك
├── 🗄️ database/
│   └── memory.py              ← حفظ واسترجاع المحادثات
├── ⚙️ config.py               ← الإعدادات والـ API Keys
├── 📋 requirements.txt        ← كل المكتبات المطلوبة
└── 📖 README.md               ← الملف ده
```

**قاعدة مهمة:** كل ملف له وظيفة واحدة بس — لو شخص بيكتب في ملف مش بتاعه، لازم يتكلم معايا الأول.

---

## 🗺 خطة التنفيذ

### المراحل الأربعة

```
المرحلة 1          المرحلة 2          المرحلة 3          المرحلة 4
التأسيس      →    التطوير      →    التكامل      →    التسليم
(أسبوعين)        (5 أسابيع)        (4 أسابيع)        (3 أسابيع)
```

---

### 🔵 المرحلة الأولى — التأسيس والإعداد
**المدة:** أسبوعين

| المهمة | المسؤول | النتيجة |
|---|---|---|
| إعداد GitHub Repo وتوزيع الـ Branches | Team Lead | الكل عارف يشتغل على GitHub |
| تثبيت البيئة البرمجية على أجهزة الكل | الكل | كل جهاز جاهز للشغل |
| إنشاء ملف `config.py` والـ API Keys | Team Lead | الـ Keys شغالة |
| تعلم Agno و Chainlit من الـ Docs | AI Developer | فهم أساسي للأدوات |
| تصميم قاعدة بيانات المحادثات | Backend Dev | Schema جاهز |

**✅ المحطة الأولى:** GitHub جاهز + البيئة شغالة عند الكل + أول "Hello World" بيشتغل

---

### 🟡 المرحلة الثانية — التطوير الأساسي
**المدة:** 5 أسابيع

| المهمة | المسؤول | النتيجة |
|---|---|---|
| بناء الـ Agent الأساسي مع Gemini | AI Developer | Agent بيستقبل سؤال ويرد |
| إضافة ArXiv Tool للـ Agent | AI Developer | Agent يبحث في الأوراق العلمية |
| إضافة DuckDuckGo Tool | AI Developer | Agent يبحث في الإنترنت |
| بناء نظام الـ Citations | AI Dev + Backend | كل إجابة فيها مصدرها |
| بناء PDF Reader | Backend Dev | النظام يقرأ ويفهم PDF |
| حفظ المحادثات في SQLite | Backend Dev | التاريخ بيتحفظ |
| بداية واجهة Chainlit الأساسية | Frontend Dev | واجهة بسيطة تشتغل |

**✅ المحطة التانية:** Agent بيبحث + يرد + يحفظ المحادثة — حتى لو الواجهة بسيطة

---

### 🟠 المرحلة التالتة — التكامل والتحسين
**المدة:** 4 أسابيع

| المهمة | المسؤول | النتيجة |
|---|---|---|
| ربط Chainlit مع الـ Agent بالكامل | الكل | النظام شغال من أوله لآخره |
| تحسين دعم اللغة العربية | AI Developer | العربي شغال بدون مشاكل |
| تحسين شكل الـ Citations في الواجهة | Frontend Dev | Citations تبان واضحة وجميلة |
| اختبار كل الـ Features | Tester | قائمة بالـ Bugs |
| إصلاح الـ Bugs اللي اتلاقت | الكل | نظام مستقر |

**✅ المحطة التالتة:** النظام الكامل شغال بكل الخصائص بدون Crashes

---

### 🔴 المرحلة الرابعة — التوثيق والتسليم
**المدة:** 3 أسابيع

| المهمة | المسؤول | النتيجة |
|---|---|---|
| كتابة الـ Documentation الكاملة | Team Lead + Documenter | README + تقرير المشروع |
| تحضير العرض التقديمي (Slides) | الكل | Presentation جاهزة |
| تجهيز الـ Demo للعرض | AI Developer | Demo شغالة بأمثلة حقيقية |
| مراجعة نهائية للكود | Team Lead | كود نظيف وموثق |
| التسليم النهائي | Team Lead | ✅ |

**✅ المحطة النهائية:** مشروع مسلم + Demo شغالة + Documentation كاملة

---

## 👥 أدوار الفريق

| الدور | المسؤوليات | الملفات |
|---|---|---|
| **Team Lead** (أنا) | GitHub + متابعة المهام + config.py + التواصل مع الدكتور | `config.py`, `README.md` |
| **AI Developer** | Agent + Gemini + أدوات البحث + Citations | `agent.py`, `tools/` |
| **Backend Developer** | قاعدة البيانات + PDF Reader + ربط الأجزاء | `database/`, `tools/pdf_tool.py` |
| **Frontend Developer** | واجهة Chainlit + تجربة المستخدم | `app.py` |
| **Tester / Documenter** | اختبار كل الـ Features + Documentation + العرض | ملفات الـ Tests |

---

## 📏 قواعد الشغل مع بعض

### قواعد GitHub — ملزمة للكل

```
❌ ممنوع تكتب مباشرة على الـ main branch
✅ كل شخص بيعمل branch باسمه للمهمة اللي بيشتغل عليها

مثال:
feature/agent-core        ← شغل الـ Agent
feature/pdf-reader        ← شغل الـ PDF
feature/chainlit-ui       ← شغل الواجهة
bugfix/arabic-encoding    ← إصلاح مشكلة
```

### الـ Commit Message — لازم يكون واضح

```
✅ "أضفت ArXiv search tool وبتجيب أول 5 نتائج"
✅ "صلحت مشكلة encoding العربي في الإجابات"
❌ "update"
❌ "fix stuff"
```

### قاعدة Scope Creep — مهمة جداً

```
لما حد يقول "ممكن نضيف خاصية كمان؟"
              ↓
السؤال الأول: هل دي Must Have؟
              ↓
     لأ → تتحط في قائمة انتظار
          ومش بتتعمل غير بعد ما
          كل المهام الأساسية تخلص
```

### الاجتماع الأسبوعي — 30 دقيقة

```
كل شخص بيقول:
1. شغلت على إيه الأسبوع الفات؟
2. في أي مشكلة بتوقفني؟
3. هشتغل على إيه الأسبوع الجاي؟
```

---

## ⚙️ إعداد البيئة — أول ما تنضم للفريق

```bash
# 1. استنسخ الـ Repo
git clone https://github.com/[team-name]/research-assistant
cd research-assistant

# 2. ثبت المكتبات
pip install agno chainlit google-generativeai arxiv duckduckgo-search pymupdf

# 3. عمل ملف الـ API Keys (مش بيتحط على GitHub أبداً)
cp config.example.py config.py
# افتح config.py وحط الـ API Key بتاعك

# 4. شغّل المشروع
chainlit run app.py
```

---

## 📊 ملخص سريع

```
المشروع:    Research Assistant Agent
الفريق:     4-5 أشخاص
المدة:      14 أسبوع
التكلفة:    صفر دولار 💰
اللغة:      Python خالص 🐍
```

---

*آخر تحديث: فبراير 2025 — للتعديلات والملاحظات تواصل مع Team Lead*
