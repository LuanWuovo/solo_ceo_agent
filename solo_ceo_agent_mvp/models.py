from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class KnowledgeTask(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(100))
    status = Column(String(20), default="processing") # processing, completed, failed
    md_content = Column(Text, nullable=True)
    action_items = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)

engine = create_engine("sqlite:///./ceo_office.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)