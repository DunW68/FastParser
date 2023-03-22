from fastapi import Depends, FastAPI, Header, HTTPException, APIRouter
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_201_CREATED
from FastParser.db.configs import Base, engine, ArticleParserSession
from fastapi_utils.cbv import cbv
from FastParser.parsers.schemas.article_parser.schemas import GetArticle, ArticleParserBase
from pydantic import AnyUrl
from FastParser.parsers.article_parser import ParseUrl
from FastParser.db.parsers.article_parser.requests import ArticleRequests


Base.metadata.create_all(bind=engine)
parser = FastAPI()
router = APIRouter(tags=["Parser"])


@cbv(router)
class ArticleParser:

    def __init__(self):
        self.article_requests = ArticleRequests(db_session=ArticleParserSession())

    @router.get("/")
    def get_article(self, url: AnyUrl) -> GetArticle:
        url_parser = ParseUrl(url=url)
        header = url_parser.get_header()
        article_text = url_parser.get_article_text()
        images = url_parser.get_article_images()
        response = GetArticle(header=header,
                             text=article_text,
                             images=images
                             )
        return response

    @router.post("/", status_code=HTTP_201_CREATED)
    def post_article(self, url: AnyUrl) -> str:
        url_parser = ParseUrl(url=url)
        header = url_parser.get_header()
        article_text = url_parser.get_article_text()
        article = ArticleParserBase(header=header, text=article_text)
        self.article_requests.create_record(article=article)
        return "Successfully parsed"


parser.include_router(router, prefix="/article_parser")
