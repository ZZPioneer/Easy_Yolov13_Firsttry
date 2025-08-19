# -*- coding: utf-8 -*-

from ultralytics import YOLO

if __name__ == '__main__':

    # Load a model
    model = YOLO(model=r'E:\Summer_intensive_study\yolo13\yolov13-main\runs\train\exp5\weights\last.pt')
    model.predict(source=r'E:\Summer_intensive_study\yolo13\yolov13-main\PCB_DATASET\PCB_USED',
                  save=True,
                  show=False,
                  # visualize=True,  # 启用检测框绘制
                  )
