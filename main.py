from fastapi import FastAPI
from starlette.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from user_manage.User_manage import *
from data_struct import *
from starlette.requests import Request
import cv2
from starlette.templating import Jinja2Templates
import threading
from Msg_auth_code import *
import db.users

lock = threading.Lock()

# 开启ip摄像头
video = "http://admin:admin@192.168.137.21:8081/video"  # 此处@后的ipv4 地址需要改为app提供的地址

templates = Jinja2Templates(directory='templates')
COUNT = 1
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/login_by_password", name="账号密码登录")
def login_by_password(user_data: Login_info):
    response = login(**user_data.dict())
    return response


@app.post("/register", name="注册")
def register_(user_data: Register_info):
    response = register(**user_data.dict())
    return response


@app.post('/login_by_phone', name="手机验证码登录")
def login_by_phone(user_data: Login_info):
    response = login(**user_data.dict())
    return response


@app.post('/send_auth_code', name="发送验证码")
def send_auth_code(user_data: Auth_code_inf):
    response = send_code(**user_data.dict())
    return response


@app.post("/items", name='测试')
def read_item(user_data: Login_info):
    print(user_data)
    return {"item_id": "bbbb"}


@app.post("/change_password", name='修改密码')
def change_password(user_data: Modify_password_inf):
    response = modify_password(**user_data.dict())
    return response


@app.post("/set_name", name='设置姓名')
def set_name(user_data: Set_user_name):
    response = set_name(**user_data.dict())
    return response


def getImg(cap):
    while True:
        ret, image_np = cap.read()
        if image_np is None:
            cap = cv2.VideoCapture(video)
            continue
        # cv2.imshow('object detection', image_np)
            # if cv2.waitKey(25) & 0xFF == ord('q'):
            #     cap.release()
            #     cv2.destroyAllWindows()
            #     print(1)
            #     break

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(cv2.imencode('.png', image_np)[1]) + b'\r\n')


@app.get('/video')
def send_video():
    return StreamingResponse(getImg(cap=cv2.VideoCapture(video)), media_type='multipart/x-mixed-replace;boundary=frame')


@app.get('/')
def f(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True, debug=True)
