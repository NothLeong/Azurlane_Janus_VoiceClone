import os

def remove_prefix_by_folder(path="."):
    # 遍历指定路径下的所有文件夹
    for root, dirs, files in os.walk(path):
        # 自动获取当前目录的最后一级名称
        folder_name = os.path.basename(os.path.normpath(root))
        prefix = folder_name + "_"
        for file in files:
            if file.startswith(prefix):
                old_path = os.path.join(root, file)
                new_name = file[len(prefix):]
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)
                print(f"✅ 重命名: {file} → {new_name}")

if __name__ == "__main__":
    # 默认在当前路径执行
    target_dir = input("请输入要处理的根目录（留空表示当前目录）: ").strip() or "."
    remove_prefix_by_folder(target_dir)
    print("\n全部处理完成 ✅")
