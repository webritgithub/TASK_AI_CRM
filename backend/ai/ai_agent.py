from langgraph.graph import StateGraph
from .state import CRMState
from .llm import llm
from .prompts import CRM_PROMPT
from .tools import (
    log_interaction,
    analyze_sentiment,
    summarize_interaction,
    generate_insight,
    next_best_action
)

import re

# =========================
# HELPER: Extract values
# =========================
def extract_value(text, label):
    match = re.search(f"{label}: (.*)", text)
    return match.group(1).strip() if match else "Unknown"


# =========================
# STEP 1: LLM Extraction
# =========================
def clean(value):
    if not value or str(value).lower() in ["unknown", "not provided", "none", "null"]:
        return None
    return value


def extract_node(state: CRMState):
    messages = CRM_PROMPT.format_messages(input=state["input"])
    response = llm.invoke(messages)

    ai_text = response.content

    return {
        **state,
        "structured": {
            "ai_output": ai_text,
            "hcp_name": clean(extract_value(ai_text, "HCP Name")),
            "interaction_type": clean(extract_value(ai_text, "Interaction Type")),
            "topics": clean(extract_value(ai_text, "Topics discussed")),
            "outcomes": clean(extract_value(ai_text, "Outcomes")),
            "follow_up": clean(extract_value(ai_text, "Follow up action"))
        }
    }


# =========================
# STEP 2: Sentiment Analysis
# =========================
def sentiment_node(state: CRMState):
    # ai_text = state.get("structured", {}).get("ai_output", "")

    # sentiment = analyze_sentiment(ai_text)
    sentiment = analyze_sentiment(state["input"])

    return {
        **state,
        "sentiment": sentiment
    }


# =========================
# STEP 3: Log Interaction
# =========================
def log_node(state: CRMState):

    structured = state.get("structured", {})

    data = {
        "hcp_name": structured.get("hcp_name"),
        "interaction_type": structured.get("interaction_type"),
        "topics": structured.get("topics"),
        "sentiment": state.get("sentiment", {}).get("sentiment", "neutral"),
        "outcomes": structured.get("outcomes"),
        "follow_up": structured.get("follow_up")
    }

    logged = log_interaction(data)

    return {
        **state,
        "logged": logged
    }


# =========================
# STEP 4: Summary
# =========================
def summary_node(state: CRMState):
    logged_data = state.get("logged", {})

    summary = summarize_interaction(logged_data)

    return {
        **state,
        "summary": summary
    }


# =========================
# STEP 5: Insight
# =========================
def insight_node(state: CRMState):
    sentiment = state.get("sentiment", {}).get("sentiment", "neutral")

    insight = generate_insight({"sentiment": sentiment})

    return {
        **state,
        "insight": insight
    }


# =========================
# STEP 6: Next Best Action
# =========================
def action_node(state: CRMState):
    sentiment = state.get("sentiment", {}).get("sentiment", "neutral")

    action = next_best_action({"sentiment": sentiment})

    return {
        **state,
        "action": action
    }


# =========================
# BUILD GRAPH
# =========================
graph = StateGraph(CRMState)

graph.add_node("extract", extract_node)
graph.add_node("sentiment", sentiment_node)
graph.add_node("log", log_node)
graph.add_node("summary", summary_node)
graph.add_node("insight", insight_node)
graph.add_node("action", action_node)

# Flow
graph.set_entry_point("extract")

graph.add_edge("extract", "sentiment")
graph.add_edge("sentiment", "log")
graph.add_edge("log", "summary")
graph.add_edge("summary", "insight")
graph.add_edge("insight", "action")

graph.set_finish_point("action")

# Compile
app_graph = graph.compile()