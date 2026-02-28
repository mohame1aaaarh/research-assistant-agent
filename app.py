import chainlit as cl
import asyncio
from agent import get_agent

# إعدادات التحكم
TYPING_SPEED = 0.03   # كل ما تقل = أسرع
CURSOR = "▌"


@cl.on_chat_start
async def start():
    agent = get_agent()
    cl.user_session.set("agent", agent)


@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")

    msg = cl.Message(content="🔍I'm thinking...")
    await msg.send()

    response = agent.run(message.content)
    full_text = response.content

    words = full_text.split()
    current_text = ""

    for word in words:
        current_text += word + " "

        # عرض النص + cursor
        msg.content = current_text + CURSOR
        await msg.update()

        await asyncio.sleep(TYPING_SPEED)

    # في النهاية نشيل الـ cursor
    msg.content = current_text.strip()
    await msg.update()