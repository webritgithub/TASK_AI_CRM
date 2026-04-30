from sqlalchemy import Column, Integer, String
from database import Base

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True)
    hcp_name = Column(String)
    interaction_type = Column(String)
    topics = Column(String)
    sentiment = Column(String)
    outcomes = Column(String)
    follow_up = Column(String)