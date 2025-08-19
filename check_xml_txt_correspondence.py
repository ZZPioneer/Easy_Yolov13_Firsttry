import os
from pathlib import Path
#这是查看文件是否一一对应

def find_missing_files(xml_dir, txt_dir):
    """
    查找缺失的XML和TXT文件，并生成详细报告

    Args:
        xml_dir (str): XML文件目录路径
        txt_dir (str): TXT文件目录路径
    """
    xml_path = Path(xml_dir)
    txt_path = Path(txt_dir)

    # 获取所有XML文件名（不含扩展名）
    xml_files = {f.stem: f.name for f in xml_path.glob("*.xml")}
    print(f"XML文件数量: {len(xml_files)}")

    # 获取所有TXT文件名（不含扩展名）
    txt_files = {f.stem: f.name for f in txt_path.glob("*.txt")}
    print(f"TXT文件数量: {len(txt_files)}")

    # 查找缺失的文件
    missing_xml = txt_files.keys() - xml_files.keys()  # 在TXT中存在但XML中缺失的文件
    missing_txt = xml_files.keys() - txt_files.keys()  # 在XML中存在但TXT中缺失的文件
    matched_files = xml_files.keys() & txt_files.keys()  # 两个集合的交集

    print("\n=== 文件对应情况 ===")
    print(f"完全对应的文件数量: {len(matched_files)}")
    print(f"XML中缺失的文件数量: {len(missing_xml)}")
    print(f"TXT中缺失的文件数量: {len(missing_txt)}")

    # 创建报告文件
    report_file = "missing_files_report.txt"

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("XML和TXT文件对应关系检查报告\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"XML文件总数: {len(xml_files)}\n")
        f.write(f"TXT文件总数: {len(txt_files)}\n")
        f.write(f"完全对应的文件数量: {len(matched_files)}\n")
        f.write(f"XML中缺失的文件数量: {len(missing_xml)}\n")
        f.write(f"TXT中缺失的文件数量: {len(missing_txt)}\n\n")

        # 列出在TXT中存在但XML中缺失的文件
        if missing_xml:
            f.write("在TXT中存在但XML中缺失的文件:\n")
            f.write("-" * 30 + "\n")
            for filename in sorted(missing_xml):
                f.write(f"{filename} (TXT: {txt_files[filename]})\n")
            f.write("\n")
        else:
            f.write("✓ 没有在TXT中存在但XML中缺失的文件\n\n")

        # 列出在XML中存在但TXT中缺失的文件
        if missing_txt:
            f.write("在XML中存在但TXT中缺失的文件:\n")
            f.write("-" * 30 + "\n")
            for filename in sorted(missing_txt):
                f.write(f"{filename} (XML: {xml_files[filename]})\n")
            f.write("\n")
        else:
            f.write("✓ 没有在XML中存在但TXT中缺失的文件\n\n")

        # 列出部分对应的文件作为参考
        f.write("部分对应的文件示例:\n")
        f.write("-" * 30 + "\n")
        for filename in sorted(matched_files)[:20]:  # 只显示前20个
            f.write(f"{filename} (XML: {xml_files[filename]}, TXT: {txt_files[filename]})\n")

        if len(matched_files) > 20:
            f.write(f"... 还有 {len(matched_files) - 20} 个对应文件\n")

    print(f"\n详细报告已保存到: {report_file}")

    # 在控制台显示缺失文件信息
    if missing_xml:
        print(f"\n=== 在TXT中存在但XML中缺失的文件 ({len(missing_xml)} 个) ===")
        for i, filename in enumerate(sorted(missing_xml), 1):
            print(f"  {i:4d}. {filename} (TXT: {txt_files[filename]})")
            if i >= 50:  # 只显示前50个
                print(f"  ... 还有 {len(missing_xml) - 50} 个文件")
                break
    else:
        print("\n✓ 没有在TXT中存在但XML中缺失的文件")

    if missing_txt:
        print(f"\n=== 在XML中存在但TXT中缺失的文件 ({len(missing_txt)} 个) ===")
        for i, filename in enumerate(sorted(missing_txt), 1):
            print(f"  {i:4d}. {filename} (XML: {xml_files[filename]})")
            if i >= 50:  # 只显示前50个
                print(f"  ... 还有 {len(missing_txt) - 50} 个文件")
                break
    else:
        print("\n✓ 没有在XML中存在但TXT中缺失的文件")

    return {
        'missing_xml': list(missing_xml),
        'missing_txt': list(missing_txt),
        'matched': len(matched_files)
    }


def save_missing_files_list(missing_data, prefix=""):
    """
    将缺失的文件列表保存到单独的文件中

    Args:
        missing_data (dict): 包含缺失文件信息的字典
        prefix (str): 文件名前缀
    """
    # 保存在TXT中存在但XML中缺失的文件列表
    if missing_data['missing_xml']:
        filename = f"{prefix}missing_xml_files.txt" if prefix else "missing_xml_files.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for file in sorted(missing_data['missing_xml']):
                f.write(f"{file}\n")
        print(f"在TXT中存在但XML中缺失的文件列表已保存到: {filename}")

    # 保存在XML中存在但TXT中缺失的文件列表
    if missing_data['missing_txt']:
        filename = f"{prefix}missing_txt_files.txt" if prefix else "missing_txt_files.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for file in sorted(missing_data['missing_txt']):
                f.write(f"{file}\n")
        print(f"在XML中存在但TXT中缺失的文件列表已保存到: {filename}")


def main():
    """
    主函数
    """
    # 定义目录路径
    xml_dir = r"E:\Summer_intensive_study\yolo13\yolov13-main\datasets2\datasets2\train\xml"
    txt_dir = r"E:\Summer_intensive_study\yolo13\yolov13-main\datasets2\datasets2\train\txt"

    # 检查目录是否存在
    if not os.path.exists(xml_dir):
        print(f"错误: XML目录不存在: {xml_dir}")
        return

    if not os.path.exists(txt_dir):
        print(f"错误: TXT目录不存在: {txt_dir}")
        return

    print("正在查找缺失的XML和TXT文件...")
    print(f"XML目录: {xml_dir}")
    print(f"TXT目录: {txt_dir}")

    # 查找缺失的文件
    missing_data = find_missing_files(xml_dir, txt_dir)

    # 保存缺失文件列表
    save_missing_files_list(missing_data)

    print("\n=== 总结 ===")
    if not missing_data['missing_xml'] and not missing_data['missing_txt']:
        print("✓ 所有XML和TXT文件一一对应")
    else:
        print("✗ XML和TXT文件不完全对应:")
        if missing_data['missing_xml']:
            print(f"  - {len(missing_data['missing_xml'])} 个文件在TXT中存在但XML中缺失")
        if missing_data['missing_txt']:
            print(f"  - {len(missing_data['missing_txt'])} 个文件在XML中存在但TXT中缺失")


if __name__ == "__main__":
    main()