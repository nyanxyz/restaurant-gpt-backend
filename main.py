from fastapi import FastAPI, HTTPException
from uuid import uuid4
import asyncio

from starlette.responses import StreamingResponse

from chatbot.controllers.chat_controller import ChatController
from chatbot.utils.chat_history import ChatHistory
import dto

app = FastAPI()
sessions = {}


@app.get("/ping")
async def ping():
    return "pong"


@app.post("/chat/start")
async def start_chat():
    session_id = str(uuid4())
    sessions[session_id] = {"history": ChatHistory()}
    return {"session_id": session_id}


@app.post("/chat/{session_id}")
async def chat(session_id: str, body: dto.Chat):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    chat_history = sessions[session_id]["history"]

    chat_controller = ChatController(chat_history)
    response = chat_controller.response(body.query)

    return StreamingResponse(response, media_type="text/event-stream")
