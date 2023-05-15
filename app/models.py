# from sqlalchemy import Column, DateTime, String, Integer, Text
# from database import Base


# class News(Base):
#     __tablename__ = 'news'
#     id = Column(Integer, primary_key=True, default=None)
#     heading = Column(String(255))
#     content = Column(Text)
#     image_url = Column(String(255))
#     publish_date = Column(DateTime)
#     source_tag = Column(String(255))
#     keywords = Column(Text)

# class Url(Base):
#     __tablename__ = "urls"
#     id = Column(Integer, primary_key=True,default=None)
#     url = Column(String(200))

from datetime import datetime
from pydantic import BaseModel

class News(BaseModel):
    id: int
    heading: str
    content: str
    image_url: str
    publish_date: datetime
    source_tag: str
    keywords: str

class Url(BaseModel):
    id: int
    url: str

