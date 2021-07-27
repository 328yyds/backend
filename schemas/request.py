from pydantic import BaseModel


class Base_info(BaseModel):
    """
    基本信息
    usertype: 用户种类
        root_user: 超级用户
        normal_root: 普通用户
    username: 用户名
    password: 密码
    """
    usertype: str
    username: str
    password: str


class Login_info(Base_info):
    """
    登录信息：
    login_type: 登录模式
        password: 用户名密码登录
        phone: 手机验证码登录
    username:用户名
    password:密码
    tel:电话
    auth_code:验证码
    """
    login_type: str
    tel: str
    auth_code: str


class Register_info(Base_info):
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
    tel: str
    auth_code: str
    admin_code: str


class Modify_password_inf(Base_info):
    """
    password: 新密码
    username: 用户名
    """
    password: str


class Auth_code_inf(BaseModel):
    tel: str


class Set_user_name(BaseModel):
    """
    usertype: 用户类型
    username: 用户名
    name: 真实姓名
    """
    usertype: str
    username: str
    name: str