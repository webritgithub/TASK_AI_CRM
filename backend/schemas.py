from pydantic import BaseModel

class InteractionCreate(BaseModel):
    hcp_name: str
    interaction_type: str
    topics: str
    sentiment: str
    outcomes: str
    follow_up: str