import io

from database.config import *
from database.table.state import *
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
data = session.query(Alarm_info_db).first().picture
x = Image.open(BytesIO(data))
print(type(x))
