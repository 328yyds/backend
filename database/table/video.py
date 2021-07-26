from sqlalchemy import Column, String, Date, Integer
from database.config import base, session, engine


class Test_video(base):
    __tablename__ = 'test_video'
    No = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    path = Column(String)

    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    @staticmethod
    def add(name: str, path: str):
        session.add(Test_video(name, path))
        session.commit()


base.metadata.create_all(engine)