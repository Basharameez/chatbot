from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import os

# Set your Google credentials path before importing genai client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credits.json"

client = genai.Client(vertexai=True, project="sahayak-465612", location="us-central1")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://basharameez.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # Combine user messages into one prompt (or customize your prompt here)
    prompt = ""
    for msg in request.messages:
        role = msg.role.capitalize()
        prompt += f"{role}: {msg.content}\n"
    prompt += "Assistant: "  # signal Gemini to respond

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return {"response": response.text.strip()}
