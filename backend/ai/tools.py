from datetime import datetime

# -------------------------
# TOOL 1: Log Interaction
# -------------------------
def log_interaction(data):
    return {
        **data,
        "timestamp": datetime.utcnow().isoformat()
    }


# -------------------------
# TOOL 2: Edit Interaction
# -------------------------
def edit_interaction(data, updates):
    data.update(updates)
    data["updated_at"] = datetime.utcnow().isoformat()
    return data


# -------------------------
# TOOL 3: Sentiment Analyzer
# -------------------------
def analyze_sentiment(text):
    text = text.lower()

    if "positive interaction" in text or "positive" in text:
        return {"sentiment": "positive"}

    if "negative interaction" in text or "negative" in text:
        return {"sentiment": "negative"}

    if any(word in text for word in ["not interested", "declined", "rejected", "refused"]):
        return {"sentiment": "negative"}

    if any(word in text for word in ["interested", "agree", "support", "good"]):
        return {"sentiment": "positive"}

    return {"sentiment": "neutral"}


# -------------------------
# TOOL 4: Summarizer
# -------------------------
# def summarize_interaction(data):
#     name = data.get("hcp_name")

#     # Handle missing name properly
#     if not name or name.lower() in ["unknown", "not specified"]:
#         name_text = "The doctor"
#     else:
#         name_text = name

#     return {
#         "summary": (
#             f"{name_text} had a "
#             f"{data.get('sentiment', 'neutral')} interaction about "
#             f"{data.get('topics', 'the product')}. "
#             f"Outcome: {data.get('outcomes', 'not specified')}."
#         )
#     }
def summarize_interaction(data):

    if not isinstance(data, dict):
        return {"summary": "Invalid data received"}

    def clean(value):
        if not value or str(value).lower() in ["none", "null", "unknown", "not provided"]:
            return None
        return value

    name = clean(data.get("hcp_name"))
    topics = clean(data.get("topics"))

    sentiment = data.get("sentiment", "neutral")
    if isinstance(sentiment, dict):
        sentiment = sentiment.get("sentiment", "neutral")

    outcomes = clean(data.get("outcomes"))

    name_text = name if name else "The doctor"

    if topics:
        summary = f"{name_text} had a {sentiment} interaction about {topics}."
    else:
        summary = f"{name_text} had a {sentiment} interaction."

    if outcomes:
        summary += f" Outcome: {outcomes}."
    else:
        summary += " Outcome: not specified."

    return {"summary": summary}


# -------------------------
# TOOL 5: Insight Generator
# -------------------------
def generate_insight(data):
    sentiment = data.get("sentiment", "neutral")

    if sentiment == "positive":
        insight = "High engagement HCP → Strong opportunity"
    elif sentiment == "negative":
        insight = "Low engagement HCP → Needs re-engagement strategy"
    else:
        insight = "Neutral engagement → Monitor interaction"

    return {"insight": insight}


# -------------------------
# TOOL 6: Next Best Action
# -------------------------
def next_best_action(data):
    sentiment = data.get("sentiment", "neutral")

    if sentiment == "positive":
        action = "Schedule follow-up meeting"
    elif sentiment == "negative":
        action = "Send educational material and revisit later"
    else:
        action = "Maintain contact and observe"

    return {"next_best_action": action}