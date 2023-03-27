from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, APIRouter
from typing import Union
from starlette.status import HTTP_201_CREATED
from FastParser.db.configs import Base, engine, ArticleParserSession
from fastapi_utils.cbv import cbv
from FastParser.parsers.schemas.article_parser.schemas import GetArticle, ArticleParserBase, ArticleImages
from pydantic import AnyUrl
from FastParser.parsers.article_parser import ParseUrl
from FastParser.db.parsers.article_parser.requests import ArticleRequests, ArticleImagesRequests


Base.metadata.create_all(bind=engine)
parser = FastAPI()
router = APIRouter(tags=["Parser"])


@cbv(router)
class ArticleParser:

    def __init__(self):
        self.article_requests = ArticleRequests(db_session=ArticleParserSession())
        self.art_images_requests = ArticleImagesRequests(db_session=ArticleParserSession())

    @router.get("/")
    def get_article(self, url: AnyUrl) -> Union[GetArticle, dict]:
        record = self.article_requests.get_record_by_url(page_url=url)
        if record:
            response = GetArticle(
                                  page_url=url,
                                  header=record.header,
                                  text=record.text,
                                  images=[image.image_url for image in record.images]
                                 )
        else:
            response = {"detail": "Article not found!"}
        return response

    @router.post("/", status_code=HTTP_201_CREATED)
    def post_article(self, url: AnyUrl) -> dict:
        url_parser = ParseUrl(url=url)
        header = url_parser.get_header()
        article_text = url_parser.get_article_text()
        article = ArticleParserBase(page_url=url, header=header, text=article_text)
        images = url_parser.get_article_images()
        images = ArticleImages(images=images)
        try:
            art_record = self.article_requests.create_record(article=article)
            self.art_images_requests.create_record(article_images=images, article_id=art_record.id)
            response = {"detail": "Successfully parsed"}
        except IntegrityError:
            response = {"detail": "Already exists"}
        return response

    @router.put("/", status_code=HTTP_201_CREATED)
    def put_article(self, url: AnyUrl) -> dict:
        parser = ParseUrl(url=url)
        article = ArticleParserBase(page_url=url, header=parser.get_header(), text=parser.get_article_text())
        images = ArticleImages(images=parser.get_article_images())
        record = self.article_requests.replace_record(page_url=url, article=article)
        if record:
            self.art_images_requests.create_record(article_images=images, article_id=record.id)
            response = {"detail": "Successfully parsed"}
        else:
            response = {"detail": "Nothing to put to. Post this article first."}
        return response

    @router.delete("/")
    def delete_article(self, page_url: AnyUrl):
        article = self.article_requests.delete_record(page_url=page_url)
        if article:
            response = {"detail": "Article deleted"}
        else:
            response = {"detail": "Article not found!"}
        return response


parser.include_router(router, prefix="/article_parser")
