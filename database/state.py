# 用户状态
from sqlalchemy import Column, String, Date, BINARY, Integer
from typing import Optional
from database.config import base, session, engine
from datetime import datetime


class Login_info_db(base):
    """
    登录信息
    """
    __tablename__ = 'Login_info'
    No = Column(Integer, primary_key=True, autoincrement=True)
    usertype = Column(String)
    username = Column(String)
    tel = Column(String)
    login_time = Column(Date)

    def __init__(self, usertype: str, username: str, tel: str, login_time: Optional[Date] = datetime.now().date()):
        self.username = username
        self.usertype = usertype
        self.tel = tel
        self.login_time = login_time

    @staticmethod
    def add(usertype, username, tel):
        session.add(Login_info_db(usertype=usertype, username=username, tel=tel))
        session.commit()


class Alarm_info_db(base):
    """
    报警信息
    """
    __tablename__ = 'alarm_info_db'

    No = Column(Integer, primary_key=True, autoincrement=True)
    invade_level = Column(String)
    invade_time = Column(Date)
    picture = Column(BINARY)

    def __init__(self, invade_level: str, picture: BINARY, invade_time: Date = datetime.now().date()):
        self.invade_time = invade_time
        self.invade_level = invade_level
        self.picture = picture

    @staticmethod
    def add(invade_level, picture):
        session.add(Alarm_info_db(invade_level, picture))
        session.commit()


base.metadata.create_all(engine)
