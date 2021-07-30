import base64
import io

import cv2
import numpy as np
from fastapi import APIRouter
from starlette.responses import StreamingResponse

from schemas.request import *
from database.table.users import *
from database.table.state import Login_info_db, Alarm_info_db
from utils import Msg_auth_code

router = APIRouter()


@router.post("/login", name="登录: 账号密码/手机验证")
def login_by_password(user_data: Login_info):
    login_type = user_data.login_type
    usertype = user_data.usertype
    username = user_data.username
    password = user_data.password
    tel = user_data.tel
    # 用户名密码登录
    if login_type == "password":
        # 管理员
        if usertype == 'root_user':
            data = session.query(Root_user_db).filter_by(username=username).all()
        # 普通用户
        else:
            data = session.query(Normal_user_db).filter_by(username=username).all()
        if len(data) == 0:
            return False, 'Username not exist'
        elif data[0].password != MD5(password):
            return False, 'Error password'
        else:
            Login_info_db.add(usertype, username, tel)
            return True, username, data[0].tel, data[0].name, 'Login successfully'
    # 手机验证码登录
    else:
        # 主页面需要获取用户的信息
        # 管理员
        if usertype == 'root_user':
            data = session.query(Root_user_db).filter_by(tel=tel).all()
        # 普通用户
        else:
            data = session.query(Normal_user_db).filter_by(tel=tel).all()
        Login_info_db.add(usertype, username, tel)
        return True, data[0].username, user_data.tel, data[0].name, 'Login successfully'


@router.post("/register", name="注册")
def register_(user_data: Register_info):
    # 普通用户注册
    usertype = user_data.usertype
    tel = user_data.tel
    username = user_data.username
    password = user_data.password
    admin_code = user_data.admin_code

    user = Normal_user_db if usertype == 'normal_user' else Root_user_db
    data = session.query(Normal_user_db).filter_by(tel=tel).all()
    if len(data) != 0:
        return False, "该手机已被注册"
    data = session.query(Root_user_db).filter_by(tel=tel).all()
    if len(data) != 0:
        return False, "该手机已被注册"
    data = session.query(Normal_user_db).filter_by(username=username).all()
    if len(data) != 0:
        return False, "该用户名已被注册"
    data = session.query(Root_user_db).filter_by(username=username).all()
    if len(data) != 0:
        return False, "该用户名已被注册"
    user.add(username=username, tel=tel, password=password, admin_code=admin_code)
    return True, 'Register successfully'


@router.post('/send_auth_code', name="发送验证码")
def send_auth_code(user_data: Auth_code_inf):
    response = Msg_auth_code.send_code(**user_data.dict())
    return response


@router.post('/delete_user', name="删除用户")
def send_auth_code(user_data: Delete_user_info):
    response = Normal_user_db.delete_user(**user_data.dict())
    return response


@router.post('/set_user_admin', name="设置管理员")
def set_admin_(user_data: Set_admin_info):
    response = Normal_user_db.set_admin(**user_data.dict())
    return response


@router.post('/set_user_head', name="设置用户头像")
def set_user_head_(user_data: User_head):
    img_base64 = user_data.img_base64
    username = user_data.username
    img_base64 = '/' + img_base64.lstrip('data:image/jpeg;base64,')
    img_data = base64.b64decode(img_base64)
    data = session.query(User_head_img).filter_by(username=username).first()
    if data is None:
        User_head_img.add(username, img_data)
    else:
        data.headImg = img_data
        session.commit()
    return True, 'Upload successfully!'


@router.get('/get_user_head/{username}', name='获取用户头像')
def get_user_head(username):
    if username == '':
        return
    data = session.query(User_head_img).filter_by(username=username).first()
    if data is None:
        return False
    return StreamingResponse(io.BytesIO(data.headImg), media_type='image/jpg')
