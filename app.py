import chainlit as cl
from agent import get_agent


# =========================
# START CHAT
# =========================
# @cl.on_chat_start
# async def start():
#     agent = get_agent()
#     cl.user_session.set("agent", agent)

#     await cl.Message(
#         content="""
# 🔬 **Welcome to Logic Lords Research Assistant**

# I can help you with:
# - 📄 Summarizing research papers
# - 🔍 Answering scientific questions
# - 📚 Providing clear explanations with sources

# 👉 Ask your question below
# """
#     ).send()# =========================سيبه حاليا مش عاجبني


# =========================
# HANDLE MESSAGE
# =========================
@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")

    # ⏳ Typing / Thinking indicator
    msg = cl.Message(content="🔍 Thinking...")
    await msg.send()

    try:
        # تشغيل الـ agent
        response = agent.run(message.content)

        # ✨ تحسين عرض الرد
        msg.content = response.content.strip()

    except Exception as e:
        # ⚠️ Error handling
        msg.content = f"""
⚠️ **Error occurred**
Something went wrong while processing your request.

Details:
{str(e)}
"""

    # 🔄 تحديث الرسالة بدل إنشاء واحدة جديدة
    await msg.update()