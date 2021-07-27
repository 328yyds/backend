from fastapi import APIRouter
from starlette.responses import StreamingResponse
from alg.behaviour_detect.tf_pose_estimation import img_process
from database.table.video import *
from database.table.state import Alarm_info_db
from alg.face_recognition.record_face import *
from alg.face_recognition.get_features import *

router = APIRouter()

COUNT = 0


def getImg(video_ip):
    """
    获取在线视频流
    :param video_ip: 摄像头IP地址
    :return:
    """
    cap = cv2.VideoCapture(video_ip)
    global COUNT
    while True:
        ret, image_np = cap.read()
        COUNT += 1
        if COUNT == 10:
            COUNT = 0
            # 检测是否翻越栅栏
            str_ = img_process(image_np)
            is_normal = face_recognition(image_np)
            print(is_normal)
            if str_ == 'jump':
                image_np = cv2.putText(image_np, "检测到翻越", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
                # 检测人脸，如果数据库里面有
                is_normal = face_recognition(image_np)
                if is_normal:
                    # 存入数据库，不发报警信息
                    Alarm_info_db.add("normal-invader", bytearray(cv2.imencode('.jpg', image_np)[1]))
                    continue
                else:  # 如果数据库里面没有这张脸
                    # 存入数据库，发送报警信息
                    image_np = cv2.putText(image_np, "陌生人入侵", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
                    Alarm_info_db.add("invader", bytearray(cv2.imencode('.jpg', image_np)[1]))
            elif str == 'walk':
                Alarm_info_db.add("normal", bytearray(cv2.imencode('.jpg', image_np)[1]))
        if image_np is None:
            cap = cv2.VideoCapture(video_ip)
            continue
        yield img2byte(image_np)


def img2byte(img):
    return (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
            bytearray(cv2.imencode('.png', img)[1]) + b'\r\n')


@router.get('/video/{ip}', name='实时传输视频')
def send_video(ip):
    return StreamingResponse(getImg('http://admin:admin@' + ip + ':8081/video'),
                             media_type='multipart/x-mixed-replace;boundary=frame')


@router.get('/video_judge/{ip}', name='判断摄像头ip是否合法')
def judge(ip):
    return cv2.VideoCapture('http://admin:admin@' + ip + ':8081/video').isOpened()


#
# @router.get('/')
# def f(request: Request):
#     return templates.TemplateResponse('index.html', {'request': request})


@router.get('/test_video/{num}', name='发送测试视频')
def get_test_video(num):
    path = session.query(Test_video).filter_by(name='test_video' + str(num))
    return StreamingResponse(getImg(path), media_type='multipart/x-mixed-replace;boundary=frame')
