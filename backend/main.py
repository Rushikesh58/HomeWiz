# backend/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
from utils import extract_info, check_inventory, send_email
from db import save_conversation, init_db, get_conversation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

class ChatInput(BaseModel):
    message: str
    session_id: Optional[str] = None

@app.post("/chat")
async def chat_endpoint(data: ChatInput):
    sid = data.session_id or "default"
    prev_data = get_conversation(sid)
    reply, updated_data = extract_info(data.message, prev_data)

    if "book" in data.message.lower() and "unit_id" in updated_data:
        send_email(updated_data)
        reply = f"Tour confirmed! Email sent to {updated_data['email']}."

    save_conversation(sid, updated_data)
    return {"reply": reply, "session_id": sid}
