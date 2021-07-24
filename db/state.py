# 用户状态
from sqlalchemy import Column, String, Date
from db.config import base, session, engine


class Login_info(base):
    __tablename__ = 'Login_info'
    usertype = Column(String)
    username = Column(String)
    tel = Column(String)
    login_time = Column(Date)

    @staticmethod
    def add(usertype, username, tel, login_time=None):
        session.add(Login_info(usertype=usertype, username=username, tel=tel, login_time=login_time))
        session.commit()


base.metadata.create_all(engine)
