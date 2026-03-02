import chainlit as cl
import asyncio
from agent import get_agent

# إعدادات التحكم
TYPING_SPEED = 0.02   # كل ما تقل = أسرع
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

    current_text = ""

    for char in full_text:
       current_text += char
       msg.content = current_text + CURSOR
       await msg.update()
       await asyncio.sleep(TYPING_SPEED)

    msg.content = current_text.strip()
    await msg.update()
    