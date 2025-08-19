#这个文件是把训练结果进行可视化
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from scipy.ndimage import gaussian_filter1d

def compare_yolo_results(results_dirs, output_path="yolo_comparison_results.png"):
    """
    将不同版本YOLO模型的训练结果图表合并到一张图中进行比较
    
    Args:
        results_dirs (dict): 包含不同版本YOLO模型结果目录的字典，格式为 {version: path}
        output_path (str): 输出图表的路径
    """
    # 定义图表标题和对应的列索引
    titles = [
        "train/box_loss", "train/cls_loss", "train/dfl_loss",
        "metrics/precision(B)", "metrics/recall(B)", 
        "metrics/mAP50(B)", "metrics/mAP75(B)", "metrics/mAP50-95(B)",
        "val/box_loss", "val/cls_loss", "val/dfl_loss"
    ]
    
    # 创建图表
    fig, axes = plt.subplots(2, 6, figsize=(24, 8))
    axes = axes.ravel()
    
    # 为每个版本绘制结果
    colors = plt.cm.tab10(np.linspace(0, 1, len(results_dirs)))
    
    for idx, (version, dir_path) in enumerate(results_dirs.items()):
        dir_path = Path(dir_path)
        csv_files = list(dir_path.glob("results*.csv"))
        
        if not csv_files:
            print(f"警告: 在 {dir_path} 中未找到 results.csv 文件")
            continue
            
        csv_file = csv_files[0]  # 使用第一个找到的CSV文件
        
        try:
            data = pd.read_csv(csv_file)
            x = data.values[:, 0]  # epoch
            
            # 选择要绘制的列索引
            # 根据ultralytics/utils/plotting.py中的index定义
            index = [2, 3, 4, 5, 6, 9, 10, 11, 7, 8, 12]  # 对应titles中的指标
            
            for i, j in enumerate(index):
                if j < data.shape[1]:  # 确保列索引不超出范围
                    y = data.values[:, j].astype("float")
                    # 绘制实际结果
                    axes[i].plot(x, y, marker=".", label=version, linewidth=2, 
                               markersize=8, color=colors[idx])
                    # 绘制平滑曲线
                    axes[i].plot(x, gaussian_filter1d(y, sigma=3), ":",
                               linewidth=2, color=colors[idx], alpha=0.7)
                    axes[i].set_title(titles[i], fontsize=10)
                    axes[i].grid(True, alpha=0.3)
                    
        except Exception as e:
            print(f"处理 {version} 的数据时出错: {e}")
    
    # 添加图例到最后一张子图
    axes[-1].axis('off')  # 关闭最后一个子图的坐标轴
    axes[-1].legend(loc='center', fontsize=12)
    
    plt.suptitle("YOLO Models Training Results Comparison", fontsize=16)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"比较图表已保存至: {output_path}")

def find_training_results_dirs(base_dir="runs/train"):
    """
    自动查找所有YOLO版本的训练结果目录
    
    Args:
        base_dir (str): 训练结果基础目录
        
    Returns:
        dict: 包含不同版本YOLO模型结果目录的字典
    """
    base_path = Path(base_dir)
    results_dirs = {}
    
    if not base_path.exists():
        print(f"基础目录 {base_dir} 不存在")
        return results_dirs
        
    # 遍历所有训练实验目录
    for exp_dir in base_path.iterdir():
        if exp_dir.is_dir():
            # 从目录名推断YOLO版本
            dir_name = exp_dir.name
            if "yolo" in dir_name.lower():
                version = dir_name.lower()
                results_dirs[version] = exp_dir
                
    return results_dirs

if __name__ == "__main__":
    # 方法1: 自动查找训练结果目录
    print("正在自动查找训练结果目录...")
    results_dirs = find_training_results_dirs()
    
    if results_dirs:
        print("找到以下训练结果目录:")
        for version, path in results_dirs.items():
            print(f"  {version}: {path}")
            
        compare_yolo_results(results_dirs, "出图的例子/yolo_models_comparison.png")
    else:
        print("未自动找到训练结果目录，请手动指定")
        # 方法2: 手动指定目录 (示例)
        # results_dirs = {
        #     "yolo_v8": "runs/train/yolov8_exp",
        #     "yolo_v9": "runs/train/yolov9_exp", 
        #     "yolo_v10": "runs/train/yolov10_exp",
        #     "yolo_v11": "runs/train/yolov11_exp",
        #     "yolo_v12": "runs/train/yolov12_exp",
        #     "yolo_v13": "runs/train/yolov13_exp"
        # }
        # compare_yolo_results(results_dirs, "yolo_models_comparison.png")