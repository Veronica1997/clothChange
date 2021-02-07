import os
import sys
import shutil
# import test


def tryon(clothimg, personimage):
    # 将人的图像拷贝到三个模型的对应文件夹下
    shutil.copy(personimage, '/home/ubuntu/00-workplace/DeepFashion_Try_On/Data_preprocessing/test_img')
    shutil.copy(personimage, '/home/ubuntu/00-workplace/AlphaPose/images')
    shutil.copy(personimage, '/home/ubuntu/00-workplace/Self-Correction-Human-Parsing-for-ACGPN-master/input')
    # 选择相应的衣服及遮罩
    sourceclothepath = '/home/ubuntu/00-workplace/DeepFashion_Try_On/Data_preprocessing/clothes/'
    sourceedgepath = '/home/ubuntu/00-workplace/DeepFashion_Try_On/Data_preprocessing/edges/'
    dstclothepath = '/home/ubuntu/00-workplace/DeepFashion_Try_On/Data_preprocessing/test_color/'
    dstedgepath = '/home/ubuntu/00-workplace/DeepFashion_Try_On/Data_preprocessing/test_edge/'
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
    # sys.path.append('/home/ubuntu/00-workplace/Self-Correction-Human-Parsing-for-ACGPN-master')
    #os.system('cd /home/ubuntu/00-workplace/Self-Correction-Human-Parsing-for-ACGPN-master')
    os.chdir("/home/ubuntu/00-workplace/Self-Correction-Human-Parsing-for-ACGPN-master")
    os.system('python simple_extractor.py')
    print(os.getcwd())
    shutil.copyfile('/home/ubuntu/00-workplace/Self-Correction-Human-Parsing-for-ACGPN-master/output/sourceImage.png',
                    '/home/ubuntu/00-workplace/DeepFashion_Try_On/Data_preprocessing/test_label', )
    sys.path.append('/home/ubuntu/00-workplace/AlphaPose')
    os.system('python scripts/demo_inference.py --cfg /home/ubuntu/00-workplace/AlphaPose/configs/coco/resnet/256x192_res152_lr1e-3_1x-duc.yaml --checkpoint /home/ubuntu/00-workplace/AlphaPose/pretrained_models/fast_421_res152_256x192.pth --indir /home/ubuntu/00-workplace/AlphaPose/images --outdir /home/ubuntu/00-workplace/AlphaPose/results --format open ')
    sys.path.append('/home/ubuntu/00-workplace/DeepFashion_Try_On/ACGPN_inference')
    os.system('python test.py')
    os.remove('/home/ubuntu/00-workplace/DeepFashion_Try_On/Data_preprocessing/test_color/clothe.jpg')
    os.remove('/home/ubuntu/00-workplace/DeepFashion_Try_On/Data_preprocessing/test_edge/clothe.jpg')
    res_path = '/home/ubuntu/00-workplace/DeepFashion_Try_On/ACGPN_inference/sample'
    return res_path


print(tryon("1.jpg", "sourceImage.jpg"))
