from pydantic import BaseModel, AnyUrl


class ArticleImages(BaseModel):
    images: list[AnyUrl]


class ArticleParserBase(BaseModel):
    page_url: AnyUrl
    header: str
    text: str

    class Config:
        orm_mode = True


class GetArticle(ArticleParserBase):
    images: list[AnyUrl]

    class Config:
        orm_mode = True
