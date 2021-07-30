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


@router.get('/invade_data_show', name='返回可视化数据')
def get_invade_data():
    response = []
    data = session.query(Alarm_info_db).order_by(Alarm_info_db.invade_time).group_by(Alarm_info_db.invade_time).all()
    data = data[-7:]
    for item in data:
        day_data = []
        day_data.append(item.invade_time)
        day_data.append(len(session.query(Alarm_info_db).filter_by(invade_time=item.invade_time).all()))
        day_data.append(len(session.query(Alarm_info_db).filter_by(invade_time=item.invade_time, invade_level=
                                                                   'invader').all()))
        day_data.append(len(session.query(Alarm_info_db).filter_by(invade_time=item.invade_time, invade_level=
                                                                   'normal').all()))
        response.append(day_data)
    return response
