from pydantic import BaseModel, AnyUrl


class ArticleParserResponse(BaseModel):
    header: str
    text: str
    images: list[AnyUrl]
