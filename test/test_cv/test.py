import cv2
from PIL import Image
from alg.behaviour_detect import *

img = cv2.imread('../../alg/behaviour_detect/a.jpg')
img = cv2.putText(img, "hello world!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
img = cv2.putText(img, "hello world!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
cv2.imwrite('a.jpg', img)
