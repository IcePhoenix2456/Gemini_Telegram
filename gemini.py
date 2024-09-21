import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

def gemini_chat(question, chat_history):
    genai.configure(api_key=os.getenv("GEMINI_API"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(history = chat_history)
    response = chat.send_message(question)
    return response.text