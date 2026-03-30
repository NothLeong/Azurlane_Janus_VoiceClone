import os

def add_prefix_by_folder(path="."):
    for root, dirs, files in os.walk(path):
        # 自动获取当前目录的最后一级名称
        folder_name = os.path.basename(os.path.normpath(root))
        prefix = folder_name + "_"

        for file in files:
            # 跳过已经有相同前缀的文件
            if not file.startswith(prefix):
                old_path = os.path.join(root, file)
                new_name = prefix + file
                new_path = os.path.join(root, new_name)

                try:
                    os.rename(old_path, new_path)
                    print(f"✅ 重命名: {file} → {new_name}")
                except Exception as e:
                    print(f"⚠️ 重命名失败: {file} ({e})")

if __name__ == "__main__":
    target_dir = input()
    add_prefix_by_folder(target_dir)
    print("\n全部处理完成 ✅")
