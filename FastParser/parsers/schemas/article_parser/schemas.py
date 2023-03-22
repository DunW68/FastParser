from pydantic import BaseModel, AnyUrl


class ArticleImage(BaseModel):
    page_url: AnyUrl
    image_url: AnyUrl
    article_id: int


class ArticleParserBase(BaseModel):
    header: str
    text: str

    class Config:
        orm_mode = True


class GetArticle(ArticleParserBase):
    images: list[AnyUrl]

    class Config:
        orm_mode = True
