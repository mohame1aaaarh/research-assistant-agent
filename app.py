import chainlit as cl
from database.auth import login_user
from database.memory import create_session, save_message, get_user_sessions, get_session_messages
import asyncio
from agent import get_agent
import config
from database.data_layer import SQLiteDataLayer
import requests

def generate_title(user_message: str) -> str:
    """Generate a short title using OpenRouter API."""
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {config.OPENROUTER_KEY}"},
            json={
                "model": "meta-llama/llama-3.1-8b-instruct:free",
                "messages": [
                    {
                        "role": "user",
                        "content": f"Generate a short 4-6 word title for a conversation that starts with: '{user_message}'. Reply with ONLY the title, no quotes, no explanation."
                    }
                ],
                "max_tokens": 20
            },
            timeout=10
        )
        return response.json()["choices"][0]["message"]["content"].strip()
    except:
        return user_message[:40]  # fallback لو فشل

@cl.data_layer
def get_data_layer():
    return SQLiteDataLayer()

TYPING_SPEED = 0.005
CURSOR = "▌"

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    result = login_user(username, password)
    if result["success"]:
        user = result["user"]
        return cl.User(identifier=username, metadata={"user_id": user["id"]})
    return None

@cl.on_chat_start
async def start():
    user = cl.user_session.get("user")
    user_id = 1  # Default fallback user ID
    
    if user and hasattr(user, "identifier"):
        from database.memory import get_user
        db_user = get_user(user.identifier)
        if db_user:
            user_id = db_user["id"]
        elif user.metadata and "user_id" in user.metadata:
            user_id = user.metadata["user_id"]

    cl.user_session.set("user_id", user_id)
    cl.user_session.set("session_id", None)  # ← مش بنعمل session هنا

    agent = get_agent()
    cl.user_session.set("agent", agent)
    await cl.Message(content="مرحباً! أنا مساعدك البحثي 🔬 اسألني أي سؤال بحثي وسأبحث لك في الأوراق العلمية والمصادر الموثوقة.").send()

@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")
    session_id = cl.user_session.get("session_id")

    # لو مفيش session، عملها دلوقتي عند أول رسالة فعلية
    if session_id is None:
        user_id = cl.user_session.get("user_id")
        session_id = create_session(user_id=user_id)
        cl.user_session.set("session_id", session_id)

    # ← ولّد العنوان في background من غير ما يأخر الرد
    from database.memory import update_session_title
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, lambda: update_session_title(session_id, generate_title(message.content)))

    # Process PDF files attached to the message
    pdf_context = ""
    if message.elements:
        import pypdf
        for element in message.elements:
            if element.mime == "application/pdf" or element.name.endswith(".pdf"):
                try:
                    reader = pypdf.PdfReader(element.path)
                    for page in reader.pages:
                        extracted = page.extract_text()
                        if extracted:
                            pdf_context += extracted + "\n"
                except Exception as e:
                    await cl.Message(content=f"⚠️ تعذر قراءة ملف PDF ({element.name}): {e}").send()
    
    final_query = message.content
    if pdf_context:
        final_query += f"\n\n[محتوى ملف PDF المرفق]:\n{pdf_context[:25000]}"

    save_message(session_id=session_id, role="user", content=message.content)

    # أرسل رسالة مؤقتة بتأثير "جاري التفكير"
    msg = cl.Message(content="⏳ جاري البحث والتحليل...")
    await msg.send()

    # ← شغّل الـ agent في thread منفصل عشان ما يقفلش الـ event loop
    response = await asyncio.get_event_loop().run_in_executor(
        None, lambda: agent.run(final_query)
    )

    if hasattr(response, "content") and response.content:
        full_text = response.content
    elif hasattr(response, "messages") and response.messages:
        full_text = response.messages[-1].content
    else:
        full_text = str(response)

    save_message(session_id=session_id, role="assistant", content=full_text)

    # تحديث الرسالة فوراً لتحسين الأداء (إزالة تأثير الكتابة البطيء)
    msg.content = full_text.strip()
    await msg.update()

@cl.on_chat_resume
async def resume(thread):
    session_id = thread["id"]
    steps = thread.get("steps", [])

    for step in steps:
        if step.get("type") == "user_message":
            await cl.Message(
                content=step.get("output", ""),
                author="You"
            ).send()
        elif step.get("type") == "assistant_message":
            await cl.Message(
                content=step.get("output", "")
            ).send()

    agent = get_agent()
    cl.user_session.set("agent", agent)
    try:
        cl.user_session.set("session_id", int(session_id))
    except (ValueError, TypeError):
        cl.user_session.set("session_id", session_id)  # keep as string