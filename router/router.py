from fastapi import APIRouter

from api.sys_user import router as user_router
from api.sys_video import router as video_router

api_router = APIRouter()

api_router.include_router(user_router, tags=['用户登录注册'])
api_router.include_router(video_router, tags=['视频传输'])