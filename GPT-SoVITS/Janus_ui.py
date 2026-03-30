# tts_server.py
from pywebio import start_server
from pywebio.input import file_upload, textarea
from pywebio.output import put_text
from pywebio_battery import put_audio
import soundfile as sf
import io

# 这里用你之前整理的最小 TTS 推理函数
def tts_infer(ref_wav_path, text):
    # ref_wav_path: str, 文本输入路径
    # text: str
    # 返回 numpy waveform
    from inference_webui import get_tts_wav  # 假设你整理好的最小函数
    wav = get_tts_wav(ref_wav_path, "all_ja", text,"all_ja")
    return wav

def main():
    put_text("Minimal TTS Web Demo (PyWeb)")

    ref_file = file_upload("Upload reference WAV", accept=".wav")
    text = textarea("Text to synthesize")

    # 保存上传的文件临时使用
    ref_path = "temp_ref.wav"
    with open(ref_path, "wb") as f:
        f.write(ref_file['content'])

    # 生成 TTS
    wav = tts_infer(ref_path, text)

    # 输出到浏览器
    out_path = "output.wav"
    sf.write(out_path, wav, 24000)
    put_audio(out_path, format='wav')

if __name__ == "__main__":
    start_server(main, port=8080, debug=True)
