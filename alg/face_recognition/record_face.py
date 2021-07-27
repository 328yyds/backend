from alg.face_recognition.get_features import get_features
from alg.face_recognition.face_recognition import *


class RecordFace:
    detector = dlib.get_frontal_face_detector()
    d = os.path.dirname(__file__)

    path_photos_from_camera = d + "/data/data_faces_from_camera/"
    path_csv_from_photos = d + "/data/data_csvs_from_camera/"

    def __init__(self):
        pass

    def record_face(self, img_rd):
        if os.listdir(self.d + "/data/data_faces_from_camera/"):
            # 获取已录入的最后一个人脸序号
            person_list = os.listdir(self.d + "/data/data_faces_from_camera/")
            person_list.sort()
            # person_num_latest = int(str(person_list[-1]).split("_")[2].split(".")[0])
            person_num_latest = int(str(person_list[-1]).split("_")[-1].split(".")[0])
            person_cnt = person_num_latest

        # 如果第一次存储或者没有之前录入的人脸, 按照 person_1 开始录入
        else:
            person_cnt = 0

        img_gray = cv2.cvtColor(img_rd, cv2.COLOR_RGB2GRAY)

        # 人脸数 faces
        faces = self.detector(img_gray, 0)

        font = cv2.FONT_HERSHEY_COMPLEX

        if len(faces) != 0:

            for k, d in enumerate(faces):
                # 计算矩形大小
                # (x,y), (宽度width, 高度height)
                pos_start = tuple([d.left(), d.top()])
                pos_end = tuple([d.right(), d.bottom()])

                # 计算矩形框大小
                height = (d.bottom() - d.top())
                width = (d.right() - d.left())

                hh = int(height / 2)
                ww = int(width / 2)

                # 设置颜色 / The color of rectangle of faces detected
                color_rectangle = (255, 255, 255)
                if (d.right() + ww) > 640 or (d.bottom() + hh > 480) or (d.left() - ww < 0) or (d.top() - hh < 0):
                    cv2.putText(img_rd, "OUT OF RANGE", (20, 300), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                    color_rectangle = (0, 0, 255)
                    save_flag = 0
                else:
                    color_rectangle = (255, 255, 255)
                    save_flag = 1

                im_blank = np.zeros((int(height * 2), width * 2, 3), np.uint8)

                if save_flag:
                    if not face_recognition(img_rd):
                        if os.path.isdir(self.d + "/data/data_faces_from_camera/"):
                            person_cnt += 1
                            for ii in range(height * 2):
                                for jj in range(width * 2):
                                    im_blank[ii][jj] = img_rd[d.top() - hh + ii][d.left() - ww + jj]
                            cv2.imwrite(
                                self.d + "/data/data_faces_from_camera/" + "/person_" + str(person_cnt) + ".jpg",
                                im_blank)
                        print("Saved successfully!")
                        return True
        print("Save failed")
        return False


def record_face(img_rd):
    face = RecordFace()
    if face.record_face(img_rd):
        get_features()
