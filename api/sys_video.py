from fastapi import APIRouter
from starlette.templating import Jinja2Templates
from starlette.responses import StreamingResponse
from starlette.requests import Request
from alg.behaviour_detect.tf_pose_estimation import img_process
from database.state import Alarm_info_db
import cv2

router = APIRouter()

video = "http://admin:admin@192.168.3.34:8081/video"  # 此处@后的ipv4 地址需要改为app提供的地址

templates = Jinja2Templates(directory='templates')
COUNT = 0


def getImg(cap):
    global COUNT
    while True:
        ret, image_np = cap.read()
        COUNT += 1
        if COUNT == 10:
            COUNT = 0
            str_ = img_process(image_np)
            if str_ == 'jump':
                print('检测到陌生人')
        if image_np is None:
            cap = cv2.VideoCapture(video)
            continue
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(cv2.imencode('.png', image_np)[1]) + b'\r\n')


@router.get('/video')
def send_video():
    return StreamingResponse(getImg(cap=cv2.VideoCapture(video)), media_type='multipart/x-mixed-replace;boundary=frame')


@router.get('/')
def f(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})
