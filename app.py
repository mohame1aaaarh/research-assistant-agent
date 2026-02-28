import chainlit as cl
from agent import get_agent  # ← هنا بتجيب الـ agent

@cl.on_chat_start
async def start():
    agent = get_agent()
    cl.user_session.set("agent", agent)


@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")
    
    msg = cl.Message(content="Processing...")
    await msg.send()
    
    response = agent.run(message.content)
    msg.content = response.content
    await msg.update()