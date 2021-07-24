from fastapi import Body
from pydantic import BaseModel


class Login_info(BaseModel):
    """
    登录信息：
    login_type: 登录模式
        password: 用户名密码登录
        phone: 手机验证码登录
    usertype: 用户种类
        root_user: 超级用户
        normal_root: 普通用户
    username:用户名
    password:密码
    tel:电话
    auth_code:验证码
    """
    login_type: str = Body(...)
    usertype: str = Body(...)
    username: str = Body(...)
    password: str = Body(...)
    tel: str = Body(...)
    auth_code: str = Body(...)


class Register_info(BaseModel):
    """
    注册信息
    usertype: 用户种类
        root_user: 超级用户
        normal_root: 普通用户
    username: 用户名
    tel: 手机号
    auth_code: 验证码
    password: 密码
    admin_code: 管理员序列码
    """
    usertype: str = Body(...)
    username: str = Body(...)
    tel: str = Body(...)
    auth_code: str = Body(...)
    password: str = Body(...)
    admin_code: str = Body(...)


class Modify_password_inf(BaseModel):
    """
    new_password: 新密码
    username: 用户名
    """
    new_password: str = Body(...)
    username: str = Body(...)
    usertype: str = Body(...)


class Auth_code_inf(BaseModel):
    tel: str = Body(...)


class Set_user_name(BaseModel):
    """
    usertype: 用户类型
    username: 用户名
    name: 真实姓名
    """
    usertype: str = Body(...)
    username: str = Body(...)
    name: str = Body(...)
