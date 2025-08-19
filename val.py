from ultralytics import YOLO

# 1. 加载你训练好的模型权重
#    通常是 runs/detect/trainX/weights/best.pt
model = YOLO("E:\Summer_intensive_study\yolo13\yolov13-main/runs/train\exp5\weights/best.pt")

# 2. 运行验证
metrics = model.val(
    data='E:\Summer_intensive_study\yolo13\yolov13-main\data.yaml',  # 同样指向你的数据集配置文件
    batch=128,
    half=True  # 使用半精度推理，可以加速
)
