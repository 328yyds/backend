from db.users import *
from icecream import ic


def login(login_type, usertype, username, password, tel, auth_code):
    # 用户名密码登录
    if login_type == "password":
        # 管理员
        if usertype == 'root_user':
            data = session.query(Root_user).filter_by(username=username).all()
        # 普通用户
        else:
            data = session.query(Normal_user).filter_by(username=username).all()
        if len(data) == 0:
            return False, 'Username not exist'
        elif data[0].password != MD5(password):
            return False, 'Error password'
        else:
            return True, username, data[0].tel, 'Login successfully'
    # 手机验证码登录
    else:
        # 主页面需要获取用户的信息
        # 管理员
        if usertype == 'root_user':
            data = session.query(Root_user).filter_by(username=username).all()
        # 普通用户
        else:
            data = session.query(Normal_user).filter_by(username=username).all()
        return True, data[0].username, tel, 'Login successfully'


def register(usertype: str, username: str, tel: str, auth_code: str, password: str, admin_code: str):
    # 普通用户注册
    user = Normal_user if usertype == 'normal_user' else Root_user
    data = session.query(user).filter_by(tel=tel).all()
    if len(data) != 0:
        return False, "该手机已被注册"
    data = session.query(user).filter_by(username=username).all()
    if len(data) != 0:
        return False, "该用户名已被注册"
    user.add(username=username, tel=tel, password=password, admin_code=admin_code)
    return True, 'Register successfully'


def modify_password(usertype, username, new_password):
    user = Normal_user if usertype == 'normal_user' else Root_user
    user.modify_password(username=username, password=new_password)
    return True, "修改成功"


def set_name(usertype, username, name):
    user = Normal_user if usertype == 'normal_user' else Root_user
    user.set_name(username=username, name=name)
    return True, "修改成功"
