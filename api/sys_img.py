from fastapi import APIRouter
from database.table.video import *
from database.table.state import *
from starlette.responses import StreamingResponse
import io
import cv2

router = APIRouter()


@router.get('/test_video_img/{num}', name='获取测试视频信息')
def get_test_video_info(num):
    data = session.query(Test_video).all()
    if num == '-1':
        return str(len(data))
    pic = cv2.VideoCapture(data[int(num)].path).read()[1]
    _, pic = cv2.imencode('.jpg', pic)
    return StreamingResponse(io.BytesIO(pic.tobytes()), media_type="image/jpg")


@router.get('/invade_img/{num}', name='返回入侵图片')
def get_invade_img(num):
    data = session.query(Alarm_info_db).all()[int(num)].picture
    return StreamingResponse(io.BytesIO(data), media_type="image/jpg")


@router.get('/invade_info', name='返回入侵详细信息')
def get_invade_info():
    data = session.query(Alarm_info_db).all()
    response = []
    for item in data:
        response.append([item.invade_level, item.invade_time])
    return response
