from pydub import AudioSegment
import os
import re

root = r"D:\Code\Python\GPT-SoVITS\Janus\raw"        # 含6个子文件夹，每个子文件夹含 mp3 + srt
output_folder = r"D:\Code\Python\GPT-SoVITS\Janus\clips"  # 所有切片统一放这里
os.makedirs(output_folder, exist_ok=True)


def parse_srt_blocks_with_time(srt_path):
    """解析 SRT 文件，返回 (start_ms, end_ms, text) 列表"""
    with open(srt_path, "r", encoding="utf-8-sig") as f:
        content = f.read()

    # 分段（空行分隔）
    blocks = re.split(r'\r?\n\r?\n+', content.strip())
    entries = []

    for block in blocks:
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if len(lines) < 2:
            continue

        # 若首行是数字编号则跳过
        if re.fullmatch(r'\d+', lines[0]):
            lines = lines[1:]
        if not lines:
            continue

        # 时间行匹配
        m = re.match(
            r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})",
            lines[0]
        )
        if not m:
            continue

        start_h, start_m, start_s, start_ms, end_h, end_m, end_s, end_ms = map(int, m.groups())
        start_ms_total = ((start_h * 60 + start_m) * 60 + start_s) * 1000 + start_ms
        end_ms_total = ((end_h * 60 + end_m) * 60 + end_s) * 1000 + end_ms

        # 合并文本行
        text = " ".join(lines[1:]).strip()
        if not text:
            continue

        entries.append((start_ms_total, end_ms_total, text))

    return entries


# 遍历 raw 下的每个角色文件夹
for subdir in os.listdir(root):
    subdir_path = os.path.join(root, subdir)
    if not os.path.isdir(subdir_path):
        continue

    print(f"🎧 正在处理文件夹：{subdir}")

    for file in os.listdir(subdir_path):
        if not file.lower().endswith((".mp3", ".wav")):
            continue

        audio_path = os.path.join(subdir_path, file)
        base = os.path.splitext(file)[0]
        srt_path = os.path.join(subdir_path, base + ".srt")

        if not os.path.exists(srt_path):
            print(f"⚠️ 未找到对应 SRT: {srt_path}")
            continue

        try:
            audio = AudioSegment.from_file(audio_path)
        except Exception as e:
            print(f"❌ 无法加载音频 {audio_path}: {e}")
            continue

        clips = parse_srt_blocks_with_time(srt_path)
        if not clips:
            print(f"⚠️ {base} 无有效字幕块，跳过。")
            continue

        clip_idx = 1
        ext = os.path.splitext(file)[1].lstrip('.')

        for start_ms, end_ms, text in clips:
            end_ms = min(end_ms, len(audio))  # 防止越界
            if start_ms >= end_ms:
                continue  # 防止空段
            clip = audio[start_ms:end_ms]
            clip_filename = f"{base}_{clip_idx}.{ext}"
            clip_path = os.path.join(output_folder, clip_filename)
            clip.export(clip_path, format=ext)
            clip_idx += 1

        print(f"✅ {base} 分割完成，共 {clip_idx - 1} 段。")

print("🎉 所有音频分割完成！")
