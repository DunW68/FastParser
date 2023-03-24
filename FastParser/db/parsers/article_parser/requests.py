from sqlalchemy.orm import Session
from FastParser.db.parsers.article_parser import models
from FastParser.parsers.schemas.article_parser import schemas


class ArticleRequests:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_record(self, article: schemas.ArticleParserBase):
        article = models.Article(page_url=article.page_url, header=article.header, text=article.text)
        self.db_session.add(article)
        self.db_session.commit()
        self.db_session.refresh(article)
        self.db_session.close()
        return article


class ArticleImagesRequests:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_record(self, article_image: schemas.ArticleImage):
        article_image = models.ImageUrls(image_url=article_image.image_url,
                                         article_id=article_image.article_id)
        self.db_session.add(article_image)
        self.db_session.commit()
        self.db_session.refresh(article_image)
        self.db_session.close()
        return article_image
