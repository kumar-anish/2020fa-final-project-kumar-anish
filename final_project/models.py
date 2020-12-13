from sqlalchemy import Column, Integer, String
from .database import Base


class QueryResult(Base):
    __tablename__ = "QueryResult"

    QueryID = Column(String(100), primary_key=True, index=True)
    MatchScore = Column(String(100))
