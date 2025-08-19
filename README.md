# YOLOv13 工具集

这个仓库包含了一系列用于处理YOLOv13目标检测模型的Python脚本和工具。这些工具涵盖了从数据预处理、训练、验证到结果可视化的完整流程。

## 目录结构

```
yolov13/
├── COCO2YOLO.py                  # COCO格式转YOLO格式标注工具
├── check_labels_in_txt_files.py  # 检查TXT标签文件有效性
├── check_xml_txt_correspondence.py # 检查XML和TXT标注文件对应关系
├── combine_yolo_results_by_metrics.py # 按指标合并多个YOLO版本训练结果
├── compare_yolo_training_results.py  # 比较不同YOLO版本训练结果
├── cuda.py                       # CUDA环境检查工具
├── detect.py                     # 目标检测推理脚本
├── divide.py                     # 数据集划分工具（训练集/验证集）
├── json_to_txt.py                # JSON标注格式转TXT格式
├── train.py                      # 模型训练脚本
├── txt_to_json.py                # TXT标注格式转JSON格式
├── val.py                        # 模型验证脚本
├── vocxml_to_yolotxt.py          # VOC XML格式转YOLO TXT格式
└── xml2yolo.py                   # XML标注转YOLO格式工具
```

## 工具说明

### 数据预处理工具

1. **COCO2YOLO.py**
   - 将COCO格式的标注数据转换为YOLO格式
   - 支持自定义输入JSON文件和输出路径

2. **vocxml_to_yolotxt.py**
   - 将VOC格式的XML标注文件转换为YOLO所需的TXT格式
   - 自动进行坐标归一化处理

3. **xml2yolo.py**
   - 另一种VOC XML到YOLO格式的转换工具
   - 支持训练集、测试集和验证集的划分

4. **json_to_txt.py**
   - 将JSON格式标注转换为TXT格式
   - 适用于LabelMe等工具生成的JSON标注

5. **txt_to_json.py**
   - TXT格式标注转换为JSON格式
   - 可用于与其他标注工具兼容

### 数据验证工具

1. **check_labels_in_txt_files.py**
   - 检查TXT标签文件是否包含有效标签框
   - 验证YOLO格式标注的正确性
   - 生成详细的检查报告

2. **check_xml_txt_correspondence.py**
   - 检查XML和TXT标注文件是否一一对应
   - 查找缺失的标注文件
   - 生成对应关系检查报告

### 训练与推理工具

1. **train.py**
   - YOLOv13模型训练脚本
   - 支持自定义模型配置和训练参数

2. **detect.py**
   - 使用训练好的模型进行目标检测推理
   - 支持批量图片检测

3. **val.py**
   - 模型验证脚本
   - 计算模型精度指标如mAP等

### 结果分析工具

1. **combine_yolo_results_by_metrics.py**
   - 将多个YOLO版本的训练结果按指标合并到一张图中
   - 支持v8、v9、v10、v11、v12、v13版本结果对比

2. **compare_yolo_training_results.py**
   - 比较不同版本YOLO模型的训练结果
   - 生成训练过程指标对比图表

### 环境检查工具

1. **cuda.py**
   - 检查CUDA环境配置
   - 显示GPU信息和可用性

### 数据集划分工具

1. **divide.py**
   - 将数据集按比例划分为训练集和验证集
   - 自动复制图像和标注文件到对应目录

## 使用方法

1. 确保已安装所需依赖：
   ```
   pip install -r requirements.txt
   ```

2. 根据需要修改各脚本中的路径配置

3. 运行相应脚本完成数据处理、训练或推理任务

## 注意事项

- 部分脚本中的路径需要根据实际环境进行修改
- 建议在运行前备份重要数据
- 某些脚本可能需要根据具体数据格式进行调整