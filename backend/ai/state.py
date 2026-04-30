from typing import TypedDict

class CRMState(TypedDict):
    input: str
    structured: dict
    sentiment: dict
    logged: dict
    summary: dict
    insight: dict
    action: dict