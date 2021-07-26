import cv2

cap = cv2.VideoCapture('../test_video/test_video_1.mp4')
_, img = cap.read()
print(type(bytearray(cv2.imencode('.png', img)[1])))