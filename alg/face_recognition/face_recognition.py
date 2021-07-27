import dlib  # 人脸处理的库 Dlib
import numpy as np  # 数据处理的库 numpy
import cv2  # 图像处理的库 OpenCv
import pandas as pd  # 数据处理的库 Pandas
import xlrd
import os


class Reco:
    d = os.path.dirname(__file__)  # 返回当前文件所在的目录
    facerec = dlib.face_recognition_model_v1(d + "/data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")
    faceList = []

    def __init__(self):
        pass

    def face_recognition(self, img_rd):
        # 处理存放所有人脸特征的 csv
        path_features_known_csv = self.d + "/data/features_all.csv"
        csv_rd = pd.read_csv(path_features_known_csv, header=None)

        # 用来存放所有录入人脸特征的数组
        features_known_arr = []

        # 读取已知人脸数据
        # known faces
        for i in range(csv_rd.shape[0]):
            features_someone_arr = []
            for j in range(0, len(csv_rd.loc[i, :])):
                features_someone_arr.append(csv_rd.loc[i, :][j])
            features_known_arr.append(features_someone_arr)

        # Dlib 检测器和预测器
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(self.d + '/data/data_dlib/shape_predictor_68_face_landmarks.dat')

        # 读取人员信息excel

        self.personList = []
        path = self.d + '/person.xlsx'

        self.get_person(path)

        # 取灰度
        img_gray = cv2.cvtColor(img_rd, cv2.COLOR_RGB2GRAY)

        # 人脸数 faces
        faces = detector(img_gray, 0)

        # 待会要写的字体
        font = cv2.FONT_HERSHEY_COMPLEX

        # 存储当前摄像头中捕获到的所有人脸的坐标/名字
        pos_namelist = []
        name_namelist = []

        # 检测到人脸
        if len(faces) != 0:
            # 获取当前捕获到的图像的所有人脸的特征，存储到 features_cap_arr
            features_cap_arr = []
            for i in range(len(faces)):
                shape = predictor(img_rd, faces[i])
                features_cap_arr.append(self.facerec.compute_face_descriptor(img_rd, shape))

            # 遍历捕获到的图像中所有的人脸
            for k in range(len(faces)):
                # 让人名跟随在矩形框的下方
                # 确定人名的位置坐标
                # 先默认所有人不认识，是 unknown
                name_namelist.append("unknown")

                # 每个捕获人脸的名字坐标
                pos_namelist.append(
                    tuple([faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 4)]))

                # 对于某张人脸，遍历所有存储的人脸特征
                for i in range(len(features_known_arr)):
                    # 将某张人脸与存储的所有人脸数据进行比对
                    compare = self.return_euclidean_distance(features_cap_arr[k], features_known_arr[i])
                    if compare == "same":  # 找到了相似脸

                        label1 = str(self.personList[i][1]) + str(self.personList[i][2])
                        name_namelist[k] = label1
                        return True
        return False

    # 计算两个128D向量间的欧式距离
    def return_euclidean_distance(self, feature_1, feature_2):
        feature_1 = np.array(feature_1)
        feature_2 = np.array(feature_2)
        dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))

        if dist > 0.4:
            return "diff"
        else:
            return "same"

    def get_person(self, path):
        # 打开execl
        workbook = xlrd.open_workbook(path)
        # 根据sheet索引或者名称获取sheet内容
        Data_sheet = workbook.sheets()[0]  # 通过索引获取
        # Data_sheet = workbook.sheet_by_index(0)  # 通过索引获取
        # Data_sheet = workbook.sheet_by_name(u'名称')  # 通过名称获取
        rowNum = Data_sheet.nrows  # sheet行数
        colNum = Data_sheet.ncols  # sheet列数

        # 获取所有单元格的内容
        for i in range(0, rowNum):
            rowlist = []
            for j in range(colNum):
                rowlist.append(Data_sheet.cell_value(i, j))
            self.personList.append(rowlist)
        return self.personList


def face_recognition(img_rd):
    recognition = Reco()
    return recognition.face_recognition(img_rd)
