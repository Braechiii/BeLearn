import os
import openai
from dotenv import load_dotenv
import chainlit as cl
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# Load your API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# LLM setup
llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo", openai_api_key=api_key)


# Socratic tutor prompt template
socratic_template = """
You are a Socratic AI tutor helping a student learn statistics.
You guide by asking thoughtful, leading questions rather than giving direct answers.
Keep your tone friendly, encouraging, and help them think critically.

Student: {student_input}
Socratic Tutor:
"""

# Setup chain
socratic_chain = LLMChain(llm=llm, prompt=ChatPromptTemplate.from_template(socratic_template))

# Log user info for experiment tracking
@cl.on_chat_start
async def start():
    # Generate and store a session ID for tracking
    session_id = cl.user_session.get("session_id")

    # Log experiment data
    print(f"New session started: {session_id} - Tutor Type: Socratic")

    await cl.Message(
        content="Welcome to the Statistics AI Tutor! 👋\n\nI'll help you learn statistics by asking guiding questions. What would you like to explore today?").send()


@cl.on_message
async def main(message: cl.Message):
    # Process the student's question
    response = await socratic_chain.arun(student_input=message.content)

    # Send response back to student
    await cl.Message(content=response).send()