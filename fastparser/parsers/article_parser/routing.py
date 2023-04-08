from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, APIRouter
from typing import Union
from starlette.status import HTTP_201_CREATED
from fastapi_utils.cbv import cbv
from fastparser.db.configs import Base, engine, ArticleParserSession
from fastparser.parsers.article_parser.schemas.schemas import GetArticle, ArticleParserBase, \
    ArticleImages
from pydantic import AnyUrl
from fastparser.parsers.article_parser.article_parser import ParseUrl
from fastparser.db.parsers.article_parser.requests import ArticleRequests, ArticleImagesRequests


Base.metadata.create_all(bind=engine)
parser = FastAPI(title="fastparser", description="Parses text and images from article.")
router = APIRouter(tags=["Parser"])


@cbv(router)
class ArticleParser:

    def __init__(self):
        self.article_requests = ArticleRequests(db_session=ArticleParserSession())
        self.art_images_requests = ArticleImagesRequests(db_session=ArticleParserSession())

    @router.get("/", summary="Gets an article")
    def get_article(self, url: AnyUrl) -> Union[GetArticle, dict]:
        """ Gets an article by page url"""
        record = self.article_requests.get_article_by_url(page_url=url)
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

    @router.post("/", status_code=HTTP_201_CREATED, summary="Parses an article")
    def post_article(self, url: AnyUrl) -> dict:
        """ Parses an article by page url and saves in db"""
        url_parser = ParseUrl(url=url)
        header = url_parser.get_header()
        article_text = url_parser.get_article_text()
        article = ArticleParserBase(page_url=url, header=header, text=article_text)
        images = url_parser.get_article_images()
        images = ArticleImages(images=images)
        try:
            art_record = self.article_requests.create_article(article=article)
            self.art_images_requests.save_image(article_images=images, article_id=art_record.id)
            response = {"detail": "Successfully parsed"}
        except IntegrityError:
            response = {"detail": "Already exists"}
        return response

    @router.put("/", status_code=HTTP_201_CREATED, summary="Updates an existing article")
    def put_article(self, url: AnyUrl) -> dict:
        """ Updates an existing article in db"""
        parser = ParseUrl(url=url)
        article = ArticleParserBase(page_url=url, header=parser.get_header(), text=parser.get_article_text())
        images = ArticleImages(images=parser.get_article_images())
        record = self.article_requests.replace_article(page_url=url, article=article)
        if record:
            self.art_images_requests.save_image(article_images=images, article_id=record.id)
            response = {"detail": "Successfully parsed"}
        else:
            response = {"detail": "Nothing to put to. Post this article first."}
        return response

    @router.delete("/", summary="Deletes article")
    def delete_article(self, page_url: AnyUrl) -> dict:
        """ Deletes article from db """
        article = self.article_requests.delete_article(page_url=page_url)
        if article:
            response = {"detail": "Article deleted"}
        else:
            response = {"detail": "Article not found!"}
        return response


page_info_router = APIRouter(tags=["Pages Info"])


@cbv(page_info_router)
class PagesInfo:

    def __init__(self):
        self.art_images_requests = ArticleImagesRequests(db_session=ArticleParserSession())

    @page_info_router.get("/related_pages", summary="Gets related pages")
    def get_article(self, url: AnyUrl, count: int = 5) -> Union[ArticleImages, dict]:
        """ Gets related pages to an article by page url """
        images = self.art_images_requests.get_related_images(page_url=url, count=count)
        if images:
            images = [image_url.image_url for image_url in images]
            response = ArticleImages(images=images)
        else:
            response = {"detail": "Images not found!"}
        return response


parser.include_router(page_info_router, prefix="/article_parser")
parser.include_router(router, prefix="/article_parser")
