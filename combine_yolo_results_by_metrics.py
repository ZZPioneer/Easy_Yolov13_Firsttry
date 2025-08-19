# -*- coding: utf-8 -*-

import warnings
warnings.filterwarnings('ignore')
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from scipy.ndimage import gaussian_filter1d

def combine_yolo_results_by_metrics():
    """
    将6个版本YOLO模型的训练结果按指标合并到一张图中进行比较
    """
    # 定义要查找的模型版本
    model_versions = ['v8', 'v9', 'v10', 'v11', 'v12', 'v13']
    
    # 定义图表标题和对应的列索引
    metrics_info = [
        ("train_box_loss", 2, "Training Box Loss"),
        ("train_cls_loss", 3, "Training Class Loss"),
        ("train_dfl_loss", 4, "Training DFL Loss"),
        ("metrics_precision", 5, "Metrics Precision (B)"),
        ("metrics_recall", 6, "Metrics Recall (B)"),
        ("metrics_map50", 9, "Metrics mAP50 (B)"),
        ("metrics_map75", 10, "Metrics mAP75 (B)"),
        ("metrics_map50_95", 11, "Metrics mAP50-95 (B)"),
        ("val_box_loss", 7, "Validation Box Loss"),
        ("val_cls_loss", 8, "Validation Class Loss"),
        ("val_dfl_loss", 12, "Validation DFL Loss")
    ]
    
    # 查找所有模型的训练结果目录
    base_dir = Path("runs/train")
    model_dirs = {}
    
    for version in model_versions:
        # 查找匹配的目录
        pattern = f"yolo{version}_exp*"
        matching_dirs = list(base_dir.glob(pattern))
        
        if matching_dirs:
            # 选择最新的目录（按名称排序）
            latest_dir = sorted(matching_dirs, reverse=True)[0]
            model_dirs[f'yolo{version}'] = latest_dir
            print(f"找到 {version} 模型结果目录: {latest_dir}")
        else:
            print(f"警告: 未找到 {version} 模型结果目录")
    
    if not model_dirs:
        print("错误: 未找到任何模型的训练结果目录")
        return
    
    # 为每个指标创建图表
    print("\n正在按指标合并图表...")
    
    # 为每个指标生成包含所有模型的图表
    colors = plt.cm.tab10(np.linspace(0, 1, len(model_dirs)))
    
    for metric_file, col_index, title in metrics_info:
        plt.figure(figsize=(12, 8))
        
        for idx, (model_name, dir_path) in enumerate(model_dirs.items()):
            csv_files = list(dir_path.glob("results*.csv"))
            
            if not csv_files:
                print(f"警告: 在 {dir_path} 中未找到 results.csv 文件")
                continue
                
            csv_file = csv_files[0]  # 使用第一个找到的CSV文件
            
            try:
                data = pd.read_csv(csv_file)
                x = data.values[:, 0]  # epoch
                
                if col_index < data.shape[1]:  # 确保列索引不超出范围
                    y = data.values[:, col_index].astype("float")
                    
                    # 绘制实际结果
                    plt.plot(x, y, marker=".", label=model_name, linewidth=2, 
                           markersize=8, color=colors[idx])
                    # 绘制平滑曲线
                    plt.plot(x, gaussian_filter1d(y, sigma=3), ":",
                           linewidth=2, color=colors[idx], alpha=0.7)
                    
            except Exception as e:
                print(f"处理 {model_name} 的 {title} 数据时出错: {e}")
                continue
        
        plt.title(f"YOLO Models Comparison - {title}", fontsize=16)
        plt.xlabel("Epoch")
        plt.ylabel(title)
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=12)
        plt.tight_layout()
        
        # 保存图表
        output_path = f"yolo_models_comparison_{metric_file}.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"图表已保存至: {output_path}")
    
    print("所有按指标合并的图表已生成完成!")

def combine_all_metrics_in_single_chart():
    """
    将所有指标合并到一个大的图表中
    """
    # 定义要查找的模型版本
    model_versions = ['v8', 'v9', 'v10', 'v11', 'v12', 'v13']
    
    # 定义图表标题和对应的列索引
    metrics_info = [
        ("train_box_loss", 2, "Training Box Loss"),
        ("train_cls_loss", 3, "Training Class Loss"),
        ("train_dfl_loss", 4, "Training DFL Loss"),
        ("metrics_precision", 5, "Metrics Precision (B)"),
        ("metrics_recall", 6, "Metrics Recall (B)"),
        ("metrics_map50", 9, "Metrics mAP50 (B)"),
        ("metrics_map75", 10, "Metrics mAP75 (B)"),
        ("metrics_map50_95", 11, "Metrics mAP50-95 (B)"),
        ("val_box_loss", 7, "Validation Box Loss"),
        ("val_cls_loss", 8, "Validation Class Loss"),
        ("val_dfl_loss", 12, "Validation DFL Loss")
    ]
    
    # 查找所有模型的训练结果目录
    base_dir = Path("runs/train")
    model_dirs = {}
    
    for version in model_versions:
        # 查找匹配的目录
        pattern = f"yolo{version}_exp*"
        matching_dirs = list(base_dir.glob(pattern))
        
        if matching_dirs:
            # 选择最新的目录（按名称排序）
            latest_dir = sorted(matching_dirs, reverse=True)[0]
            model_dirs[f'yolo{version}'] = latest_dir
        else:
            print(f"警告: 未找到 {version} 模型结果目录")
    
    if not model_dirs:
        print("错误: 未找到任何模型的训练结果目录")
        return
    
    # 创建一个大的图表，包含所有指标
    fig, axes = plt.subplots(3, 4, figsize=(24, 18))
    axes = axes.ravel()
    
    # 确保不超过子图数量
    metrics_info = metrics_info[:min(len(metrics_info), len(axes))]
    
    # 为每个指标绘制所有模型的数据
    colors = plt.cm.tab10(np.linspace(0, 1, len(model_dirs)))
    
    for metric_idx, (metric_file, col_index, title) in enumerate(metrics_info):
        for model_idx, (model_name, dir_path) in enumerate(model_dirs.items()):
            csv_files = list(dir_path.glob("results*.csv"))
            
            if not csv_files:
                continue
                
            csv_file = csv_files[0]  # 使用第一个找到的CSV文件
            
            try:
                data = pd.read_csv(csv_file)
                x = data.values[:, 0]  # epoch
                
                if col_index < data.shape[1]:  # 确保列索引不超出范围
                    y = data.values[:, col_index].astype("float")
                    
                    # 绘制实际结果
                    axes[metric_idx].plot(x, y, marker=".", label=model_name, linewidth=2, 
                                        markersize=6, color=colors[model_idx])
                    # 绘制平滑曲线
                    axes[metric_idx].plot(x, gaussian_filter1d(y, sigma=3), ":",
                                        linewidth=2, color=colors[model_idx], alpha=0.7)
                    axes[metric_idx].set_title(title, fontsize=12)
                    axes[metric_idx].grid(True, alpha=0.3)
                    axes[metric_idx].tick_params(labelsize=10)
                    
            except Exception as e:
                print(f"处理 {model_name} 的 {title} 数据时出错: {e}")
                continue
    
    # 隐藏多余的子图
    for i in range(len(metrics_info), len(axes)):
        axes[i].axis('off')
    
    # 在最后一个子图位置添加图例
    axes[-1].axis('off')
    axes[-1].legend(loc='center', fontsize=12)
    
    plt.suptitle("YOLO Models Training Results Comparison by Metrics", fontsize=20)
    plt.tight_layout()
    
    # 保存图表
    output_path = "出图的例子/yolo_models_all_metrics_comparison.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"完整比较图表已保存至: {output_path}")

if __name__ == '__main__':
    print("YOLO多版本模型训练结果按指标合并图表脚本")
    print("1. 为每个指标生成包含所有模型的图表")
    print("2. 生成包含所有指标和模型的综合图表")
    
    combine_yolo_results_by_metrics()
    combine_all_metrics_in_single_chart()
    
    print("\n所有图表合并操作已完成!")