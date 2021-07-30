import cv2
import requests
from fastapi import APIRouter
from starlette.responses import StreamingResponse
from database.table.video import *
from concurrent.futures import ThreadPoolExecutor, as_completed
from alg.detect_area.detect_area import *
from alg.behaviour_detect.behaviour_detect import detect_behaviour

import torch

if torch.cuda.is_available():
    torch.cuda.get_device_properties(0)

router = APIRouter()
COUNT = 0


def img2byte(img):
    return (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
            bytearray(cv2.imencode('.png', img)[1]) + b'\r\n')


@router.get('/video_area/{ip}', name='实时传输视频: 检测区域')
def send_video(ip):
    data = str(ip).split(':')
    return StreamingResponse(
        get_img_detect_area('http://admin:admin@' + data[0] + ':8081/video', int(data[1].split('=')[1]),
                            int(data[2].split('=')[1]), int(data[3].split('=')[1]), int(data[4].split('=')[1])),
        media_type='multipart/x-mixed-replace;boundary=frame')


@router.get('/video_behaviour/{ip}', name='实时传输视频: 检测人物动作')
def send_video(ip):
    return StreamingResponse(
        detect_behaviour('http://admin:admin@' + ip + ':8081/video'),
        media_type='multipart/x-mixed-replace;boundary=frame')


@router.get('/video_judge/{ip}', name='判断摄像头ip是否合法')
def judge(ip):
    size = len(session.query(Vidicon).filter_by(ip=ip).all())
    if size > 0:
        return cv2.VideoCapture('http://admin:admin@' + ip + ':8081/video').isOpened()
    else:
        return "not register"


def get_test_video1(num):
    path = session.query(Test_video).filter_by(name='video_' + str(num)).first()
    if path is None:
        return None
    path = path.path
    cap = cv2.VideoCapture(path)
    success, frame = cap.read()
    while success:
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(cv2.imencode('.png', frame)[1]) + b'\r\n')
        success, frame = cap.read()


@router.get('/test_video/{num}', name='发送测试视频')
def get_test_video(num):
    return StreamingResponse(get_test_video1(num), media_type='multipart/x-mixed-replace;boundary=frame')


@router.get('/register_video/{ip}', name='注册摄像头')
def register_video(ip):
    data = session.query(Vidicon).filter_by(ip=ip).all()
    if len(data) > 0:
        return False, '该摄像头已存在'
    is_available = cv2.VideoCapture('http://admin:admin@' + ip + ':8081/video').isOpened()
    if is_available:
        Vidicon.add(ip)
        return True, '摄像头注册成功'
    return False, '该摄像头无法访问'


@router.get('/search_available_ip', name='查找当前可用ip')
def search_available_ip():
    data = session.query(Vidicon).all()
    response = []
    for item in data:
        state = []
        try:
            state.append(item.ip)
            requests.get('http://admin:admin@' + item.ip + ':8081/video', timeout=0.5, stream=True)
            state.append('available')
        except requests.exceptions.ConnectTimeout:
            state.append('unavailable')
        response.append(state)
    return response
