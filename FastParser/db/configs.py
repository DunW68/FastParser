from sqlalchemy.engine import URL, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

article_parser_url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="admin",
    host="localhost",
    port=5432,
    database="articleparser",
)

engine = create_engine(article_parser_url)

ArticleParserSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()