from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from fastparser.db.configs import Base


class Article(Base):
    __tablename__ = "articleparser"

    id = Column(Integer, primary_key=True, index=True)
    page_url = Column(String, unique=True)
    header = Column(String, default=None)
    text = Column(String, default=None)
    parsed_date = Column(DateTime, default=datetime.utcnow())

    images = relationship("ImageUrls", back_populates="articles", cascade="all,delete")


class ImageUrls(Base):
    __tablename__ = "articleimages"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, unique=True)
    article_id = Column(Integer, ForeignKey("articleparser.id"))

    articles = relationship("Article", back_populates="images")
