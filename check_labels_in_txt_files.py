import os
from pathlib import Path

def check_labels_in_txt_files(txt_dir):
    """
    检查TXT标签文件是否包含标签框
    
    Args:
        txt_dir (str): TXT文件目录路径
    """
    txt_path = Path(txt_dir)
    
    # 获取所有TXT文件
    txt_files = list(txt_path.glob("*.txt"))
    print(f"找到 {len(txt_files)} 个TXT文件")
    
    if not txt_files:
        print("目录中没有找到TXT文件")
        return
    
    # 统计变量
    files_with_labels = 0
    files_without_labels = 0
    total_labels = 0
    empty_files = []
    invalid_format_files = []
    valid_files = []
    
    print("\n正在检查每个文件中的标签...")
    
    # 检查每个文件
    for i, txt_file in enumerate(txt_files, 1):
        if i % 100 == 0 or i == len(txt_files):
            print(f"进度: {i}/{len(txt_files)} ({i/len(txt_files)*100:.1f}%)")
        
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 去除空行和只包含空白字符的行
            labels = [line.strip() for line in lines if line.strip()]
            
            if len(labels) == 0:
                # 文件为空
                files_without_labels += 1
                empty_files.append(txt_file.name)
            else:
                # 检查标签格式
                valid_labels = 0
                for label in labels:
                    parts = label.split()
                    # YOLO格式要求至少5个部分: class_id cx cy w h
                    if len(parts) >= 5:
                        try:
                            # 检查数值是否有效
                            values = [float(x) for x in parts[1:5]]
                            # 检查坐标是否在0-1范围内
                            if all(0 <= v <= 1 for v in values):
                                valid_labels += 1
                        except ValueError:
                            # 数值转换失败
                            pass
                
                if valid_labels > 0:
                    files_with_labels += 1
                    total_labels += valid_labels
                    valid_files.append((txt_file.name, valid_labels))
                else:
                    files_without_labels += 1
                    invalid_format_files.append(txt_file.name)
                    
        except Exception as e:
            print(f"处理文件 {txt_file.name} 时出错: {e}")
            files_without_labels += 1
            invalid_format_files.append(txt_file.name)
    
    # 输出统计结果
    print("\n" + "="*60)
    print("检查结果统计")
    print("="*60)
    print(f"总文件数: {len(txt_files)}")
    print(f"包含有效标签的文件数: {files_with_labels}")
    print(f"不包含有效标签的文件数: {files_without_labels}")
    print(f"总标签数: {total_labels}")
    
    if files_with_labels > 0:
        print(f"平均每文件标签数: {total_labels/files_with_labels:.2f}")
    
    # 详细信息
    if empty_files:
        print(f"\n空文件数: {len(empty_files)}")
        if len(empty_files) <= 20:
            print("空文件列表:")
            for filename in empty_files:
                print(f"  - {filename}")
        else:
            print("空文件列表 (前20个):")
            for filename in empty_files[:20]:
                print(f"  - {filename}")
            print(f"  ... 还有 {len(empty_files) - 20} 个文件")
    
    if invalid_format_files:
        print(f"\n格式无效文件数: {len(invalid_format_files)}")
        if len(invalid_format_files) <= 20:
            print("格式无效文件列表:")
            for filename in invalid_format_files:
                print(f"  - {filename}")
        else:
            print("格式无效文件列表 (前20个):")
            for filename in invalid_format_files[:20]:
                print(f"  - {filename}")
            print(f"  ... 还有 {len(invalid_format_files) - 20} 个文件")
    
    # 显示一些有效文件的示例
    if valid_files:
        print(f"\n有效文件示例 (前10个):")
        for filename, count in valid_files[:10]:
            print(f"  - {filename}: {count} 个标签")
    
    # 保存报告
    save_report(txt_dir, files_with_labels, files_without_labels, total_labels, 
                empty_files, invalid_format_files, valid_files)
    
    return {
        'total_files': len(txt_files),
        'files_with_labels': files_with_labels,
        'files_without_labels': files_without_labels,
        'total_labels': total_labels,
        'empty_files': empty_files,
        'invalid_format_files': invalid_format_files
    }

def save_report(txt_dir, files_with_labels, files_without_labels, total_labels,
                empty_files, invalid_format_files, valid_files):
    """
    保存检查报告到文件
    """
    report_file = "labels_check_report.txt"
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("TXT标签文件检查报告\n")
        f.write("="*50 + "\n\n")
        
        f.write(f"检查目录: {txt_dir}\n")
        f.write(f"总文件数: {files_with_labels + files_without_labels}\n")
        f.write(f"包含有效标签的文件数: {files_with_labels}\n")
        f.write(f"不包含有效标签的文件数: {files_without_labels}\n")
        f.write(f"总标签数: {total_labels}\n")
        
        if files_with_labels > 0:
            f.write(f"平均每文件标签数: {total_labels/files_with_labels:.2f}\n")
        
        f.write("\n空文件列表:\n")
        f.write("-" * 30 + "\n")
        if empty_files:
            for filename in empty_files:
                f.write(f"{filename}\n")
        else:
            f.write("无\n")
        
        f.write("\n格式无效文件列表:\n")
        f.write("-" * 30 + "\n")
        if invalid_format_files:
            for filename in invalid_format_files:
                f.write(f"{filename}\n")
        else:
            f.write("无\n")
        
        f.write("\n有效文件示例:\n")
        f.write("-" * 30 + "\n")
        for filename, count in valid_files[:50]:  # 保存前50个示例
            f.write(f"{filename}: {count} 个标签\n")
    
    print(f"\n详细报告已保存到: {report_file}")

def main():
    """
    主函数
    """
    # 定义目录路径
    txt_dir = r"E:\Summer_intensive_study\yolo13\yolov13-main\datasets2\datasets2\train\txt"
    
    # 检查目录是否存在
    if not os.path.exists(txt_dir):
        print(f"错误: TXT目录不存在: {txt_dir}")
        return
    
    print(f"正在检查目录中的标签文件: {txt_dir}")
    
    # 检查标签
    result = check_labels_in_txt_files(txt_dir)
    
    print("\n" + "="*60)
    print("总结")
    print("="*60)
    if result['files_with_labels'] == result['total_files']:
        print("✓ 所有文件都包含有效的标签框")
    elif result['files_with_labels'] > 0:
        print(f"⚠️ {result['files_with_labels']}/{result['total_files']} 文件包含有效标签")
        print(f"  {result['files_without_labels']} 个文件没有有效标签")
    else:
        print("✗ 没有任何文件包含有效标签")

if __name__ == "__main__":
    main()