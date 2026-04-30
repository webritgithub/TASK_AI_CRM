from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ai.ai_agent import app_graph
from ai.tools import edit_interaction

import routes.interaction_routes as interaction_routes
from database import SessionLocal
import models
from ai.llm import llm

app = FastAPI(title="AI-First CRM")

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROUTES
# =========================
app.include_router(interaction_routes.router)

# =========================
# REQUEST MODEL
# =========================
class ChatRequest(BaseModel):
    message: str


# =========================
# AI CHAT (LangGraph)
# =========================
@app.post("/ai/chat")
def chat(req: ChatRequest):
    result = app_graph.invoke({
        "input": req.message,
        "structured": {},
        "sentiment": {},
        "logged": {},
        "summary": {},
        "insight": {},
        "action": {}
    })
    return result


# =========================
# AI EDIT INTERACTION 
# =========================
@app.put("/ai/edit/{id}")
def ai_edit(id: int, payload: dict = Body(...)):
    try:
        db = SessionLocal()

        interaction = db.query(models.Interaction).filter(models.Interaction.id == id).first()

        if not interaction:
            return {"error": "Interaction not found"}

        existing_data = {
            "hcp_name": interaction.hcp_name,
            "interaction_type": interaction.interaction_type,
            "topics": interaction.topics,
            "sentiment": interaction.sentiment,
            "outcomes": interaction.outcomes,
            "follow_up": interaction.follow_up
        }

        instruction = payload.get("instruction", "")

        # AI EDIT using LLM
        prompt = f"""
You are a CRM AI assistant.

Existing Interaction:
{existing_data}

User Instruction:
{instruction}

Return updated fields only in this format:

sentiment:
follow_up:
"""

        response = llm.invoke(prompt)

        text = response.content

        def extract(label):
            import re
            match = re.search(f"{label}: (.*)", text)
            return match.group(1).strip() if match else None

        updates = {
            "sentiment": extract("sentiment"),
            "follow_up": extract("follow_up")
        }

        # remove None values
        updates = {k: v for k, v in updates.items() if v}

        updated_data = edit_interaction(existing_data, updates)

        # Save to DB
        for key, value in updated_data.items():
            setattr(interaction, key, value)

        db.commit()
        db.refresh(interaction)

        return interaction

    except Exception as e:
        return {"error": str(e)}