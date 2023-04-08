from sqlalchemy.orm import Session
from fastparser.db.configs import Base


class BaseRequests:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def commit_record(self, record: Base):
        self.db_session.add(record)
        self.db_session.commit()
        self.db_session.refresh(record)

    def delete_record(self, record: Base):
        self.db_session.delete(record)
        self.db_session.commit()

    def __del__(self):
        self.db_session.close()
