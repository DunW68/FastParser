from sqlalchemy.orm import Session
from FastParser.db.parsers.article_parser import models
from FastParser.parsers.schemas.article_parser import schemas


class ArticleRequests:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_record(self, article: schemas.ArticleParserBase) -> models.Article:
        article = models.Article(page_url=article.page_url, header=article.header, text=article.text)
        self.db_session.add(article)
        self.db_session.commit()
        self.db_session.refresh(article)
        self.db_session.close()
        return article

    def get_record_by_url(self, page_url) -> models.Article:
        record = self.db_session.query(models.Article).filter(
                                                              models.Article.page_url == page_url
                                                             ).first()
        return record


class ArticleImagesRequests:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_record(self, article_images: schemas.ArticleImages, article_id) -> schemas.ArticleImages:
        for article_image in article_images.images:
            article_image = models.ImageUrls(image_url=article_image,
                                             article_id=article_id)
            self.db_session.add(article_image)
            self.db_session.commit()
            self.db_session.refresh(article_image)
            self.db_session.close()
        return article_images
