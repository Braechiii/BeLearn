import os
import openai
from dotenv import load_dotenv
import chainlit as cl

# Load your API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Chainlit setup for interactive UI
@cl.on_chat_start
async def setup():
    cl.user_session.set("messages", [
        {"role": "system", "content": "You are a helpful, knowledgeable instructor tutor that explains concepts clearly, patiently, and concisely."}
    ])

@cl.on_message
async def main(message: cl.Message):
    messages = cl.user_session.get("messages")
    messages.append({"role": "user", "content": message.content})

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=800
    )

    answer = response.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})

    await cl.Message(content=answer).send()
