from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from FastParser.db.configs import Base


class Article(Base):
    __tablename__ = "articleparser"

    id = Column(Integer, primary_key=True, index=True)
    header = Column(String, default=None)
    text = Column(String, default=None)
    # image_id = Column(Integer, ForeignKey("articleimages.id"))

    images = relationship("ImageUrls", back_populates="articles")


class ImageUrls(Base):
    __tablename__ = "articleimages"

    id = Column(Integer, primary_key=True, index=True)
    page_url = Column(String)
    image_url = Column(String)
    article_id = Column(Integer, ForeignKey("articleparser.id"))

    articles = relationship("Article", back_populates="images")
