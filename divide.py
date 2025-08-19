# -*- coding: utf-8 -*-

import os, shutil
from sklearn.model_selection import train_test_split


val_size = 0.2
postfix = 'jpg'
imgpath = r'E:\Summer_intensive_study\yolo13\yolov13-main\PCB_DATASET\images\all_img'#这里是原始照片的路径
txtpath =  r'E:\Summer_intensive_study\yolo13\yolov13-main\PCB_DATASET\Annotations\label_txt'#这里是标注文件的路径，即txt文件路径



output_train_img_folder =r'C:\Users\Administrator\Desktop\shujuji\dataset_kengwa/images/train'#这里只要修改到/images的路径就行，img前面会有一个文件夹路径，代码会自动进行创建可以选择在图片的根目录下
output_val_img_folder =  r'C:\Users\Administrator\Desktop\shujuji\dataset_kengwa/images/val'
output_train_txt_folder =  r'C:\Users\Administrator\Desktop\shujuji\dataset_kengwa\labels/train'
output_val_txt_folder =  r'C:\Users\Administrator\Desktop\shujuji\dataset_kengwa\labels/val'

os.makedirs(output_train_img_folder, exist_ok=True)
os.makedirs(output_val_img_folder, exist_ok=True)
os.makedirs(output_train_txt_folder, exist_ok=True)
os.makedirs(output_val_txt_folder, exist_ok=True)


listdir = [i for i in os.listdir(txtpath) if 'txt' in i]
train, val = train_test_split(listdir, test_size=val_size, shuffle=True, random_state=0)


for i in train:
    img_source_path = os.path.join(imgpath, '{}.{}'.format(i[:-4], postfix))
    txt_source_path = os.path.join(txtpath, i)

    img_destination_path = os.path.join(output_train_img_folder, '{}.{}'.format(i[:-4], postfix))
    txt_destination_path = os.path.join(output_train_txt_folder, i)

    shutil.copy(img_source_path, img_destination_path)
    shutil.copy(txt_source_path, txt_destination_path)

for i in val:
    img_source_path = os.path.join(imgpath, '{}.{}'.format(i[:-4], postfix))
    txt_source_path = os.path.join(txtpath, i)

    img_destination_path = os.path.join(output_val_img_folder, '{}.{}'.format(i[:-4], postfix))
    txt_destination_path = os.path.join(output_val_txt_folder, i)

    shutil.copy(img_source_path, img_destination_path)
    shutil.copy(txt_source_path, txt_destination_path)

