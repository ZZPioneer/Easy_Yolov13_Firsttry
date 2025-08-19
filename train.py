# -*- coding: utf-8 -*-

import warnings
warnings.filterwarnings('ignore')
from ultralytics import YOLO

if __name__ == '__main__':


    model = YOLO(model=r'E:\Summer_intensive_study\yolo13\yolov13-main\ultralytics\cfg\models\v13\yolov13.yaml')
    #model.load('yolov13n.pt') # 加载预训练权重,改进或者做对比实验时候不建议打开，因为用预训练模型整体精度没有很明显的提升
    #model.tune(data='data.yaml', hyp='default.yaml')
    model.train(data=r'data.yaml',
                imgsz=640,#该参数代表输入图像的尺寸，指定为 640x640 像素
                epochs=50,#该参数代表训练的轮数，官网默认是300
                batch=-1,#该参数代表训练的批次数，该参数代表批处理大小，电脑显存越大，就设置越大，根据自己电脑性能设置
                workers=0,#该参数代表数据加载的工作线程数，出现显存爆了的话可以设置为0，默认是8
                device='0',#该参数代表训练设备，默认是cpu，如果电脑有gpu，可以设置为gpu，如'0'
                optimizer='ADAM',#该参数代表优化器类型
                close_mosaic=10,#该参数代表是否使用马赛克，默认是10，该参数代表在多少个 epoch 后关闭 马赛克 数据增强
                resume=False,#该参数代表是否从上一次中断的训练状态继续训练。设置为False表示从头开始新的训练。如果设置为True，则会加载上一次训练的模型权重和优化器状态，继续训练。这在训练被中断或在已有模型的基础上进行进一步训练时非常有用。
                project='runs/train',#该参数代表项目文件夹，用于保存训练结果
                name='exp',#该参数代表训练结果文件夹名称
                single_cls=False,#该参数代表是否单类别训练，设置为True表示只训练一个类别，设置为False表示训练多个类别
                cache=False,#该参数代表是否缓存数据，设置为True表示将数据缓存到内存中，提高训练速度，但需要更多的内存。
                )

