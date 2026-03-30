import os, subprocess
from config import python_exec

env = os.environ.copy()
env.update({
    "gpt_path": "GPT_weights_v2Pro\Janus-e20.ckpt",
    "sovits_path": "SoVITS_weights_v2Pro\Janus_e12_s720.pth",
    "cnhubert_base_path": "GPT_SoVITS/pretrained_models/chinese-hubert-base",
    "bert_path": "GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large",
    "_CUDA_VISIBLE_DEVICES": "0",
    "is_half": "True",
    "is_share": "False",
})

# 注意这里的 --server-name 127.0.0.1 很关键！
cmd = f'"{python_exec}" -s .\GPT_SoVITS\inference_webui.py zh_CN --server-name 127.0.0.1 --server-port 9872'
subprocess.run(cmd, shell=True, env=env)
