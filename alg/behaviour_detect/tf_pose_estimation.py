import numpy as np
import cv2
import tflite_runtime.interpreter as tflite
from PIL import Image, ImageFont, ImageDraw
import os


def paint_chinese_opencv(im, chinese, pos, color):
    img_PIL = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    font = ImageFont.truetype('NotoSansCJK-Bold.ttc', 25, encoding="utf-8")
    fillColor = color  # (255,0,0)
    position = pos  # (100,100)
    draw = ImageDraw.Draw(img_PIL)
    draw.text(position, chinese, fillColor, font)

    return cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)


def get_angle(v1, v2):
    angle = np.dot(v1, v2) / (np.sqrt(np.sum(v1 * v1)) * np.sqrt(np.sum(v2 * v2)))
    angle = np.arccos(angle) / 3.14 * 180

    cross = v2[0] * v1[1] - v2[1] * v1[0]
    if cross < 0:
        angle = - angle
    return angle


def get_pos(keypoints):
    height = keypoints[1][1] - keypoints[16][0]
    # 计算左腿夹角
    v1 = keypoints[11][1] - keypoints[13][1]
    # 计算右腿夹角
    v2 = keypoints[12][1] - keypoints[14][1]
    print(v1, v2, height)
    if abs((v1 + v2) / height) / 2 < 0.1:
        return 'jump'
    return 'normal'


'''
配置信息
'''
# 检测模型
file_model = "posenet_mobilenet_v1.tflite"
file_model = '\\'.join(os.path.abspath(file_model).split('\\')[:-1]) + '\\alg\\behaviour_detect\\' + file_model
interpreter = tflite.Interpreter(model_path=file_model)
interpreter.allocate_tensors()

# 获取输入、输出的数据的信息
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# 获取PosNet 要求输入图像的高和宽
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]


def img_process(img):
    # 获取图像帧的尺寸
    imH, imW, _ = np.shape(img)

    # BGR 转RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 尺寸缩放适应PosNet 网络输入要求
    img_resized = cv2.resize(img_rgb, (width, height))
    # 维度扩张适应网络输入要求
    input_data = np.expand_dims(img_resized, axis=0)
    # 尺度缩放 变为 -1~+1
    input_data = (np.float32(input_data) - 128.0) / 128.0
    # 数据输入网络
    interpreter.set_tensor(input_details[0]['index'], input_data)
    # 进行关键点检测
    interpreter.invoke()
    # 获取hotmat
    hotmaps = interpreter.get_tensor(output_details[0]['index'])[0]  # Bounding box coordinates of detected objects
    # 获取偏移量
    offsets = interpreter.get_tensor(output_details[1]['index'])[0]  # Class index of detected objects
    # 获取hotmat的 宽 高 以及关键的数目
    h_output, w_output, n_KeyPoints = np.shape(hotmaps)
    # 存储关键点的具体位置
    keypoints = []
    # 关键点的置信度
    score = 0
    for i in range(n_KeyPoints):
        # 遍历每一张hotmap
        hotmap = hotmaps[:, :, i]
        # 获取最大值 和最大值的位置
        max_index = np.where(hotmap == np.max(hotmap))
        max_val = np.max(hotmap)
        # 获取y，x偏移量 前n_KeyPoints张图是y的偏移 后n_KeyPoints张图是x的偏移
        offset_y = offsets[max_index[0], max_index[1], i]
        offset_x = offsets[max_index[0], max_index[1], i + n_KeyPoints]
        # 计算在posnet输入图像中具体的坐标
        pos_y = max_index[0] / (h_output - 1) * height + offset_y
        pos_x = max_index[1] / (w_output - 1) * width + offset_x
        # 计算在源图像中的坐标
        pos_y = pos_y / (height - 1) * imH
        pos_x = pos_x / (width - 1) * imW
        # 取整获得keypoints的位置
        keypoints.append([int(round(pos_x[0])), int(round(pos_y[0]))])
        # 利用sigmoid函数计算置每一个点的置信度
        score = score + 1.0 / (1.0 + np.exp(-max_val))

    # 取平均得到最终的置信度
    score = score / n_KeyPoints
    str_pos = ""
    if score > 0.5:
        # 标记关键点
        for point in keypoints:
            cv2.circle(img, (point[0], point[1]), 5, (255, 255, 0), 5)
        # 画关节连接线
        # 左臂
        cv2.polylines(img, [np.array([keypoints[5], keypoints[7], keypoints[9]])], False, (0, 255, 0), 3)
        # # 右臂
        cv2.polylines(img, [np.array([keypoints[6], keypoints[8], keypoints[10]])], False, (0, 0, 255), 3)
        # # 左腿
        cv2.polylines(img, [np.array([keypoints[11], keypoints[13], keypoints[15]])], False, (0, 255, 0), 3)
        # # 右腿
        cv2.polylines(img, [np.array([keypoints[12], keypoints[14], keypoints[16]])], False, (0, 255, 255), 3)
        # 身体部分
        cv2.polylines(img, [np.array([keypoints[5], keypoints[6], keypoints[12], keypoints[11], keypoints[5]])],
                      False, (255, 255, 0), 3)
        # 计算位置角
        str_pos = get_pos(keypoints)
    return str_pos
    # 显示动作识别结果
    # img = paint_chinese_opencv(img, str_pos, (0, 5), (255, 0, 0))
    # cv2.imwrite('Pos.jpg', img)


# img_process(cv2.imread('a.jpg'))
