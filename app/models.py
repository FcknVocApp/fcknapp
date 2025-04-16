from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class WordEntry(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, index=True)
    translation = Column(String)
    example_en = Column(String)
    example_ru = Column(String)
    mistakes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)