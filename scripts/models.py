from sqlalchemy import Column, DateTime, String, Integer, Text
from database import Base

class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True, default=None)
    heading = Column(String(255))
    content = Column(Text)
    image_url = Column(String(255))
    publish_date = Column(DateTime)
    source_tag = Column(String(255))

class Url(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True,default=None)
    url = Column(String(200))