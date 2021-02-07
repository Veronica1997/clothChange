#-*-coding:utf-8-*-
import socket
import os
import sys
import struct
import os
import sys
import shutil
# import test
# import demo_inference.py


def socket_service_image():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 6001))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    print("Wait for Connection.....................")
    global flag
    flag = 2
    while flag:
        sock, addr = s.accept()  # addr是一个元组(ip,port)
        deal_image(sock, addr)
        flag -= 1

    print(fn)
    tryon(fn, "sourceImage.jpg")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 6001))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    print("Wait for Connection.....................")
    sock, addr = s.accept()
    while 1:
        filepath = "./sample/sourceImage.jpg"  # 输入当前目录下的图片名 xxx.jpg
        fhead = struct.pack(b'128sq', bytes(os.path.basename(filepath), encoding='utf-8'),
                            os.stat(filepath).st_size)  # 将xxx.jpg以128sq的格式打包
        sock.send(fhead)

        fp = open(filepath, 'rb')  # 打开要传输的图片
        while True:
            data = fp.read(1024)  # 读入图片数据
            if not data:
                print('{0} send over...'.format(filepath))
                break
            sock.send(data)  # 以二进制格式发送图片数据
    # while True:
    #      sock, addr = s.accept()  # addr是一个元组(ip,port)
    #      deal_image(sock, addr)



def deal_image(sock, addr):
    global fn
    print("Accept connection from {0}".format(addr))  # 查看发送端的ip和端口
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


def tryon(clothimg, personimage):
    # 将人的图像拷贝到模型的对应文件夹下
    shutil.copy(personimage, '/home/ubuntu/00-workplace/ClothChange/Data_preprocessing/test_img')
    shutil.copy(personimage, '/home/ubuntu/00-workplace/ClothChange/ACGPN_inference/images')
    shutil.copy(personimage, '/home/ubuntu/00-workplace/ClothChange/ACGPN_inference/input')
    # 选择相应的衣服及遮罩
    sourceclothepath = '/home/ubuntu/00-workplace/ClothChange/Data_preprocessing/clothes'
    sourceedgepath = '/home/ubuntu/00-workplace/ClothChange/Data_preprocessing/edges'
    dstclothepath = '/home/ubuntu/00-workplace/ClothChange/Data_preprocessing/test_color'
    dstedgepath = '/home/ubuntu/00-workplace/ClothChange/Data_preprocessing/test_edge'
    for root, dirs, files in os.walk(sourceclothepath):
        for name in files:
            if clothimg in name:
                shutil.copyfile(os.path.join(root, name),
                                os.path.join(dstclothepath, "clothe.jpg"))
    for root, dirs, files in os.walk(sourceedgepath):
        for name in files:
            if clothimg in name:
                shutil.copyfile(os.path.join(root, name),
                                os.path.join(dstedgepath, "clothe.jpg"))
    # 获得人体标签
    os.system('python simple_extractor.py')
    # 获得人体姿态
    # os.chdir('/home/ubuntu/00-workplace/ClothChange/ACGPN_inference')
    os.system('python demo_inference.py --cfg /home/ubuntu/00-workplace/ClothChange/ACGPN_inference/configs/coco/resnet/256x192_res152_lr1e-3_1x-duc.yaml --checkpoint /home/ubuntu/00-workplace/ClothChange/ACGPN_inference/pretrained_models/fast_421_res152_256x192.pth --format open')
    # 换衣
    shutil.copy('/home/ubuntu/00-workplace/ClothChange/ACGPN_inference/examples/res/sep-json/sourceImage.json', '/home/ubuntu/00-workplace/ClothChange/Data_preprocessing/test_pose/sourceImage_keypoints.json')
    os.system('python test.py')
    # 清除已选择衣服
    os.remove('/home/ubuntu/00-workplace/ClothChange/Data_preprocessing/test_color/clothe.jpg')
    os.remove('/home/ubuntu/00-workplace/ClothChange/Data_preprocessing/test_edge/clothe.jpg')
    # res_path = '/home/ubuntu/00-workplace/ACGPN_inference/sample'


if __name__ == '__main__':
    socket_service_image()


