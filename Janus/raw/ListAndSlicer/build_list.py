import os
import re

audio_folder = r"D:\Code\Python\GPT-SoVITS\Janus\clips"
srt_root = r"D:\Code\Python\GPT-SoVITS\Janus\raw"
output_list_file = r"D:\Code\Python\GPT-SoVITS\Janus\clips\slicer.list"

def parse_srt_texts(srt_path):
    """返回 SRT 文本列表，顺序与切片一一对应"""
    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    blocks = re.split(r'\r?\n\r?\n+', content.strip())
    texts = []
    for block in blocks:
        lines = block.strip().splitlines()
        if len(lines) < 3:
            continue
        # 第三行开始是字幕文本，如果有多行就合并
        text = ' '.join(lines[2:]).strip()
        texts.append(text)
    return texts

def clip_index_key(filename):
    """
    从形如 '常服_登录_12.mp3' 提取序号 12 作为排序键。
    若没有匹配到则返回 0（使之排在最前或可保证稳定排序）。
    """
    m = re.search(r'_(\d+)\.mp3$', filename, flags=re.IGNORECASE)
    if m:
        return int(m.group(1))
    # 退而求其次：尝试最后一段下划线后取数字
    parts = filename.rsplit('_', 1)
    if len(parts) == 2:
        tail = parts[1]
        tail = tail.lower().removesuffix('.mp3')
        if tail.isdigit():
            return int(tail)
    return 0

with open(output_list_file, 'w', encoding='utf-8') as f:
    # 遍历 raw 下每个子文件夹（srt 文件可能都在各自子文件夹）
    for subdir in os.listdir(srt_root):
        subdir_path = os.path.join(srt_root, subdir)
        if not os.path.isdir(subdir_path):
            continue

        print(f"📘 正在处理目录：{subdir_path}")

        for srt_file in os.listdir(subdir_path):
            if not srt_file.lower().endswith('.srt'):
                continue

            base = os.path.splitext(srt_file)[0]  # e.g. "常服_登录"
            srt_path = os.path.join(subdir_path, srt_file)
            texts = parse_srt_texts(srt_path)

            # 寻找对应的切片文件：以 base_ 开头的 mp3，例如 "常服_登录_1.mp3"
            prefix = base + "_"
            clip_files = [cf for cf in os.listdir(audio_folder)
                          if cf.lower().endswith('.mp3') and cf.startswith(prefix)]

            if not clip_files:
                print(f"⚠️ 警告：在 clips 中未找到与 SRT 匹配的切片，前缀 = {prefix}")
                continue

            clip_files = sorted(clip_files, key=clip_index_key)

            for i, clip_file in enumerate(clip_files):
                text = texts[i] if i < len(texts) else "[unknown]"
                audio_path = os.path.join(audio_folder, clip_file)
                # 写入绝对路径（Windows 风格）和标签
                line = f"{audio_path}|raw|JA|{text}\n"
                f.write(line)

print("✅ slicer.list 文件生成完成！")
