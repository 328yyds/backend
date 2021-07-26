from fastapi import APIRouter
from schemas.request import *
from database.table.users import *

router = APIRouter()


@router.post("/change_password", name='修改密码')
def change_password(user_data: Modify_password_inf):
    usertype = user_data.usertype
    username = user_data.username
    new_password = user_data.password
    user = Normal_user_db if usertype == 'normal_user' else Root_user_db
    user.modify_password(user, username=username, password=new_password)
    return True, "修改成功"


@router.post("/set_user_name", name='设置真实姓名')
def set_user_name_(user_data: Set_user_name):
    usertype = user_data.usertype
    username = user_data.username
    name = user_data.name
    user = Normal_user_db if usertype == 'normal_user' else Root_user_db
    user.set_name(user, username=username, name=name)
    return True, "修改成功"
