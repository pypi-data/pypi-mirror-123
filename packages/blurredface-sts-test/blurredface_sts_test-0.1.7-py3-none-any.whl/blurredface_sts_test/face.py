import importlib

import cv2
from cv2 import face
import matplotlib.pyplot as plt
import numpy as np

import blurredface_sts_test
import os

import importlib.resources as pkgresources


def prinfPath():
    print(os.path.dirname(os.path.realpath(__file__)) + "\haarcascades\haarcascade_frontalface_default.xml")

def prinfABC():
    print("ABC")

def prinfLsd():
    print("lsd" + "abc")

def prinfOs():
    print(os.path.dirname(os.path.realpath(__file__)))

#打码函数
# size为打码的方块大小
def drawMask(x_start,x_end,y_start,y_end,size,img):
    #为了让码好看一些,做了一个size*size的分区处理
    for m in range(y_start,y_end):  #马赛克
        for n in range(x_start,x_end):
            if m%size==0 and n%size==0 :
                for i in range(size):
                    for j in range(size):
                        b,g,r=img[m,n]
                        img[m+i,n+j]=(b,g,r)


def faceRecognizer(filepath):
    # 读取图片
    img = cv2.imread(filepath)
    # img = cv2.resize(img,(1920,1080),interpolation=cv2.INTER_CUBIC)

    # parent = os.path.dirname(os.path.realpath(__file__))

    # 转换成灰度图像
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.namedWindow('recognizer')
    # OpenCV人脸识别分类器
    classifier_default = cv2.CascadeClassifier(
        #"haarcascades/haarcascade_frontalface_default.xml"
        # "haarcascade_frontalface_default.xml"
        # blurredface_sts_test.haarcascade.haarcascade_frontalface_default
        # parent+"\haarcascades\haarcascade_frontalface_default.xml"
        "haarcascade_frontalface_default.xml"
        # pkgresources.path(blurredface_sts_test, "haarcascade_frontalface_default.xml")

    )
    classifier_alt_tree = cv2.CascadeClassifier(
        # "haarcascades/haarcascade_frontalface_alt_tree.xml"
        # "haarcascade_frontalface_alt_tree.xml"
        # blurredface_sts_test.haarcascade.haarcascade_frontalface_alt_tree
        # parent + "\haarcascades\haarcascade_frontalface_alt_tree.xml"
        "haarcascade_frontalface_alt_tree.xml"
        # pkgresources.path(blurredface_sts_test, "haarcascade_frontalface_alt_tree.xml")
    )
    classifier_alt2 = cv2.CascadeClassifier(
        # "haarcascades/haarcascade_frontalface_alt2.xml"
        # "haarcascade_frontalface_alt2.xml"
        # blurredface_sts_test.haarcascade.haarcascade_frontalface_alt2
        # parent+"\haarcascades\haarcascade_frontalface_alt2.xml"
        "haarcascade_frontalface_alt2.xml"
        # pkgresources.path(blurredface_sts_test, "haarcascade_frontalface_alt2.xml")
    )
    classifier_alt = cv2.CascadeClassifier(
        # "haarcascades/haarcascade_frontalface_alt.xml"
        # "haarcascade_frontalface_alt.xml"
        # blurredface_sts_test.haarcascade.haarcascade_frontalface_alt
        # parent + "\haarcascades\haarcascade_frontalface_alt.xml"
        "haarcascade_frontalface_alt.xml"
        # pkgresources.path(blurredface_sts_test, "haarcascade_frontalface_alt.xml")
    )
    classifier_ce = cv2.CascadeClassifier(
        # "haarcascades/haarcascade_profileface.xml"
        # "haarcascade_profileface.xml"
        # blurredface_sts_test.haarcascade.haarcascade_profileface
        # parent+"\haarcascades\haarcascade_profileface.xml"
        "haarcascade_profileface.xml"
        # pkgresources.path(blurredface_sts_test, "haarcascade_profileface.xml")
    )
    color = (0, 0, 255)  # 定义绘制颜色
    # 调用识别人脸
    faceRects_default = classifier_default.detectMultiScale(gray_img, scaleFactor=1.3, minNeighbors=0)
    faceRects_alt_tree = classifier_alt_tree.detectMultiScale(gray_img, scaleFactor=1.3, minNeighbors=0)
    faceRects_alt2 = classifier_alt2.detectMultiScale(gray_img, scaleFactor=1.4, minNeighbors=0)
    faceRects_alt = classifier_alt.detectMultiScale(gray_img, scaleFactor=1.4, minNeighbors=0)
    faceRects_ce = classifier_ce.detectMultiScale(gray_img, scaleFactor=1.4, minNeighbors=0)

    list1 = [faceRects_default, faceRects_alt_tree, faceRects_alt2, faceRects_alt, faceRects_ce]
    color = (0, 0, 255)  # 定义绘制颜色
    # 遍历图片，画出人脸矩形
    face_length = sum([len(i) for i in list1])
    if face_length > 0:
        for face in list1:
            for (x, y, w, h) in face:
                # 框出人脸,2为矩形边框线的粗细像素。厚度-1像素将以指定的颜色填充矩形形状。
                # cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
                drawMask(x, x + w, y, y + h, 5, img)
    # 图片处理、显示
    plt.figure(figsize=(10, 5), dpi=80)
    plt.imshow(img[:, :, [2, 1, 0]])
    #     plt.savefig("save/"+filepath,dpi=300)
    plt.show()



