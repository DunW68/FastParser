from fastapi import Depends, FastAPI, Header, HTTPException, APIRouter
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from fastapi_utils.cbv import cbv
from FastParser.parsers.models.article_parser.schemas import ArticleParserResponse
from pydantic import AnyUrl
from FastParser.parsers.article_parser import ParseUrl


parser = FastAPI()
router = APIRouter(tags=["Parser"])


@cbv(router)
class ArticleParser:

    @router.get("/")
    def parse_article(self, url: AnyUrl) -> ArticleParserResponse:
        url_parser = ParseUrl(url=url)
        header = url_parser.get_header()
        article_text = url_parser.get_article_text()
        images = url_parser.get_article_images()
        response = ArticleParserResponse(header=header,
                                         text=article_text,
                                         images=images
                                         )
        return response


parser.include_router(router, prefix="/article_parser")
