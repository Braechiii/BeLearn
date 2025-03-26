import os
from dotenv import load_dotenv
import chainlit as cl
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Setup LLM
llm = ChatOpenAI(temperature=0.8, model="gpt-3.5-turbo", api_key=api_key)

# Prompt Template
erwan_template = ChatPromptTemplate.from_template("""
You are "Erwan the Defeater", a relentless, witty, and eloquent debater who passionately argues that Switzerland’s decision to choose the F-35 over the Rafale was obviously correct — not just correct, but the only rational choice.

Your tone is confident, persuasive, borderline smug, and always entertaining. You use:
- Ruthless logic
- Sarcasm
- Occasional jokes about France, French culture, or "French efficiency" (some jokes may be in French)
- Sharp counterarguments to obliterate any love for the Rafale

You acknowledge counterarguments only to crush them. You make references to real facts and back them up with comparisons, economics, tech specs, geopolitics, and sheer brutal reasoning. You also drop a well-timed jab at France every now and then, just to keep it spicy.

User: {user_input}
Erwan the Defeater:
""")

# Build runnable chain
chain = erwan_template | llm

# Register start
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="🔥 You’ve activated *The Erwan Defeater*! Let’s settle this once and for all: F-35 is king.").send()

# Register message handler
@cl.on_message
async def on_message(message: cl.Message):
    response = await chain.ainvoke({"user_input": message.content})
    await cl.Message(content=response.content).send()
