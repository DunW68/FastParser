from sqlalchemy.engine import URL, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def create_db_url(database):
    db_url = URL.create(
        drivername="postgresql+psycopg2",
        username="postgres",
        password="admin",
        host="postgres",
        port=5432,
        database=database,
    )
    return db_url


engine = create_engine(create_db_url("articleparser"))

ArticleParserSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()