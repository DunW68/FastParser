from sqlalchemy.exc import IntegrityError, PendingRollbackError
from FastParser.db.parsers.article_parser import models
from FastParser.parsers.schemas.article_parser import schemas
from pydantic import AnyUrl
from datetime import datetime
from FastParser.db.base import BaseRequests


class ArticleRequests(BaseRequests):

    def __init__(self, db_session, model=models.Article):
        super(ArticleRequests, self).__init__(db_session=db_session)
        self.model = model

    def create_article(self, article: schemas.ArticleParserBase) -> models.Article:
        article = self.model(page_url=article.page_url,
                             header=article.header,
                             text=article.text)
        self.commit_record(record=article)
        return article

    def get_article_by_url(self, page_url) -> models.Article:
        record = self.db_session.query(self.model).filter(self.model.page_url == page_url).first()
        return record

    def replace_article(self, page_url, article: schemas.ArticleParserBase):
        record = self.get_article_by_url(page_url=page_url)
        if record:
            record.header = article.header
            record.text = article.text
            record.page_url = article.page_url
            record.parsed_date = datetime.utcnow()
            self.commit_record(record=record)
        return record

    def delete_article(self, page_url: AnyUrl):
        record = self.get_article_by_url(page_url=page_url)
        if record:
            self.delete_record(record=record)
        return record


class ArticleImagesRequests(BaseRequests):

    def __init__(self, db_session, model=models.ImageUrls):
        super(ArticleImagesRequests, self).__init__(db_session=db_session)
        self.model = model

    def save_image(self, article_images: schemas.ArticleImages, article_id) -> schemas.ArticleImages:
        for article_image in article_images.images:
            try:
                article_image = self.model(image_url=article_image, article_id=article_id)
                self.commit_record(record=article_image)
            except (IntegrityError, PendingRollbackError):
                continue
        return article_images
