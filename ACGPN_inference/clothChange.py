#-*-coding:utf-8-*-
import os
import sys
import shutil
# import test
# import demo_inference.py

def tryon(clothimg, personimage):
    # 将人的图像拷贝到模型的对应文件夹下
    shutil.copy(personimage, '/home/ubuntu/00-workplace/ClothChange/Data_preprocessing/test_img')
    shutil.copy(personimage, '/home/ubuntu/00-workplace/ClothChange/ACGPN_inference/images')
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


print(tryon("1.jpg", "sourceImage.jpg"))