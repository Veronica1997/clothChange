# -*- coding: utf-8 -*-
import socket
import os
import sys
import struct
import cv2
import time

def getSourceImageFromCamera(imageWidth,imageHeight,imageSavePath):
    """
    :param imageWidth:the width of imagey
    :param imageHeight:the height of image
    :param imageSavePath: the path should be saved
    :return: imagepath
    """
    camera = cv2.VideoCapture(0)
    while(1):
        _,frame = camera.read()
        cv2.rectangle(frame, (110, 40), (110+imageWidth,40+imageHeight), (0, 0, 255), 1)
        cv2.imshow("put your body in the red box and press y to confirm", frame)
        if cv2.waitKey(1) & 0xFF == ord('y'):
            cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
            sourceImage = frame[40+1:40+imageHeight-1, 110+1:110+imageWidth-1]
            cv2.imwrite(imageSavePath, sourceImage)
            break
    camera.release()
    cv2.destroyAllWindows()
    return imageSavePath


def sock_client_image():
    global flag
    flag = 2
    while flag:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('139.186.201.199', 6000))  #服务器和客户端在不同的系统或不同的主机下时使用的ip和端口，首先要查看服务器所在的系统网卡的ip
            # s.connect(('127.0.0.1', 6666))  #服务器和客户端都在一个系统下时使用的ip和端口
        except socket.error as msg:
            print(msg)
            print(sys.exit(1))
        if flag==2:
            filepath = input('input the person file: ')   #输入当前目录下的人像图片名 xxx.jpg
        if flag==1:
            filepath = input('input the clothe file: ')  # 输入当前目录下的服装图片名 xxx.jpg
        fhead = struct.pack(b'128sq', bytes(os.path.basename(filepath), encoding='utf-8'), os.stat(filepath).st_size)  #将xxx.jpg以128sq的格式打包
        s.send(fhead)

        fp = open(filepath, 'rb')  #打开要传输的图片
        while True:
            data = fp.read(1024) #读入图片数据
            if not data:
                print('{0} send over...'.format(filepath))
                break
            s.send(data)  #以二进制格式发送图片数据
        flag -= 1
        s.close()


def sock_rev_image():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('139.186.201.199', 6001))  # 服务器和客户端在不同的系统或不同的主机下时使用的ip和端口，首先要查看服务器所在的系统网卡的ip
            # s.connect(('127.0.0.1', 6666))  #服务器和客户端都在一个系统下时使用的ip和端口
        except socket.error as msg:
            print(msg)
            print(sys.exit(1))
        print("已连接")
        while True:
            deal_image(s)


def deal_image(sock):
    global fn
    # print("Accept connection from {0}".format(addr))  # 查看发送端的ip和端口
    fileinfo_size = struct.calcsize('128sq')
    buf = sock.recv(fileinfo_size)  # 接收图片名
    if buf:
        filename, filesize = struct.unpack('128sq', buf)
        fn = filename.decode().strip('\x00')
        recvd_size = 0
        fp = open(fn, 'wb')

        while not recvd_size == filesize:
            if filesize - recvd_size > 1024:
                data = sock.recv(1024)
                recvd_size += len(data)
            else:
                data = sock.recv(1024)
                recvd_size = filesize
            fp.write(data)  # 写入图片数据
        fp.close()
        #sock.close()
           # break




if __name__ == '__main__':
    getSourceImageFromCamera(382, 412, "1.jpg")
    sock_client_image()
    time.sleep(60)
    sock_rev_image()

