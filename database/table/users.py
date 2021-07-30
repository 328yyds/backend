# 用户信息
import hashlib

from sqlalchemy import Column, String, Date, Integer, BINARY
from database.config import base, session, engine
from datetime import datetime


# 对密码进行加密
def MD5(password):
    md5 = hashlib.md5(b'12345')  # 生成MD5对象 并加盐
    md5.update(password.encode('utf-8'))  # 对数据加密
    return md5.hexdigest()


# 基类
class Base_user(base):
    __abstract__ = True
    No = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    name = Column(String, default="")
    tel = Column(String, unique=True)
    password = Column(String, nullable=False)
    last_login_time = Column(Date, nullable=True)

    def __init__(self, username: str, tel: str, password: str,
                 last_login_time: datetime.date, name: str = None):
        self.username = username
        self.name = name
        self.tel = tel
        self.password = password
        self.last_login_time = last_login_time

    # 修改密码
    @staticmethod
    def modify_password(table, username: str, password: str):
        session.query(table).filter_by(username=username).update({'password': MD5(password)})
        session.commit()

    # 设置姓名
    @staticmethod
    def set_name(table, username: str, name: str):
        session.query(table).filter_by(username=username).update({'name': name})
        session.commit()


class Root_user_db(Base_user):
    __tablename__ = 'root_user'
    admin_code = Column(String)

    def __init__(self, username: str, tel: str, password: str,
                 last_login_time: datetime.date, admin_code: str, name: str = ""):
        super().__init__(username=username, name=name, tel=tel, password=password,
                         last_login_time=last_login_time)
        self.admin_code = admin_code

    @staticmethod
    def add(username: str, tel: str, password: str, admin_code: str,
            last_login_time: datetime.date = datetime.now().date()):
        session.add(Root_user_db(username=username, tel=tel, password=MD5(password),
                                 admin_code=admin_code, last_login_time=last_login_time))
        session.commit()

    @staticmethod
    # 用于在设置管理员时对已加密的密码不进行再次加密
    def set_password(username: str, password: str):
        session.query(Root_user_db).filter_by(username=username).update({'password': password})
        session.commit()


class Normal_user_db(Base_user):
    __tablename__ = 'normal_user'

    def __init__(self, username: str, tel: str, password: str,
                 last_login_time: datetime.date, admin_code: str = "", name: str = ""):
        super().__init__(username=username, name=name, tel=tel, password=password,
                         last_login_time=last_login_time)

    @staticmethod
    def add(username: str, tel: str, password: str, admin_code: str,
            last_login_time: datetime.date = datetime.now().date()):
        session.add(Normal_user_db(username=username, tel=tel, password=MD5(password),
                                   last_login_time=last_login_time))
        session.commit()

    @staticmethod
    def delete_user(username: str):
        session.query(Normal_user_db).filter_by(username=username).delete()
        session.commit()
        return True, 'Delete successfully!'

    @staticmethod
    def set_admin(username: str):
        user = session.query(Normal_user_db).filter_by(username=username).first()
        Root_user_db.add(user.username, user.tel, user.password, '001', user.last_login_time)
        Root_user_db.set_password(user.username, user.password)
        Root_user_db.set_name(Root_user_db, username, user.name)
        session.query(Normal_user_db).filter_by(username=username).delete()
        session.commit()
        return True, 'Set successfully!'


class User_head_img(base):
    __tablename__ = 'user_head_img'
    No = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    headImg = Column(BINARY)

    def __init__(self, username: str, headImg: BINARY):
        self.headImg = headImg
        self.username = username

    @staticmethod
    def add(username, headImg):
        session.add(User_head_img(username, headImg))
        session.commit()


base.metadata.create_all(engine)
