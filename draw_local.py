import os
import time
import requests
import base64
import hashlib
from datetime import datetime
from difflib import SequenceMatcher
from PIL import Image

API_URL = "https://zh.wsw233.com/api/tools/mfsc_special/draw"
RESULT_DIR = "result"
COUNT = 1
README_FILE = "README.md"

SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")

os.makedirs(RESULT_DIR, exist_ok=True)

def ocr_extract_label(img_path, max_retries=3):
    with open(img_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    
    url = "https://api.siliconflow.cn/v1/chat/completions"
    payload = {
        "model": "Qwen/Qwen2-VL-72B-Instruct",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "请识别图片左下角区域的所有文字内容。包括关卡名称、难度评价等所有信息；如果未能识别到文字，则尝试识别其他地方的醒目文字；如果还是识别不到，就返回 unknown。直接返回识别的文字，不要做任何解释。"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
            ]
        }],
        "max_tokens": 512,
        "temperature": 0.1
    }
    headers = {"Authorization": f"Bearer {SILICONFLOW_API_KEY}", "Content-Type": "application/json"}
    
    for attempt in range(max_retries):
        resp = requests.post(url, json=payload, headers=headers)
        
        if resp.status_code == 429 or "RPM limit" in resp.text:
            wait_time = 15 * (attempt + 1)
            print(f"  OCR限速触发，等待 {wait_time} 秒...")
            time.sleep(wait_time)
            continue
        
        if resp.ok:
            text = resp.json()["choices"][0]["message"]["content"]
            text = text.strip().replace('\n', '-').replace('\r', '-')
            for c in '/\\:*?"<>|':
                text = text.replace(c, '')
            return text
        else:
            print(f"OCR失败: {resp.text[:100]}")
            time.sleep(5)
    
    return "unknown"

def draw():
    resp = requests.post(API_URL)
    data = resp.json()
    
    if data.get("code") not in [0, 1]:
        print(f"抽取失败: {data.get('message')}")
        return None
    
    code = data["code"]
    image_data = data["image"]
    
    if code == 0:
        if "," in image_data:
            image_data = image_data.split(",", 1)[1]
        img_bytes = base64.b64decode(image_data)
        img_hash = hashlib.md5(img_bytes).hexdigest()[:8]
        
        temp_path = os.path.join(RESULT_DIR, "temp.jpg")
        with open(temp_path, "wb") as f:
            f.write(img_bytes)
        
        label = ocr_extract_label(temp_path)
        os.remove(temp_path)
        
        filename = f"{label}_{img_hash}.jpg"
        filepath = os.path.join(RESULT_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(img_bytes)
        
        print(f"有效抽取: {filename}")
        return (label, filename)
    elif code == 1:
        print("无效抽取，停止")
        return False

def update_readme(new_items):
    if not os.path.exists(README_FILE):
        content = "# 已收集的节气挂命图\n\n"
    else:
        with open(README_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    
    if not content.endswith('\n'):
        content += '\n'
    
    for label in new_items:
        line = f"- {label}"
        if line not in content:
            content += line + "\n"
    
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"已更新 README.md")

print(f"[{datetime.now()}] 开始抽取...")

if os.path.exists(RESULT_DIR):
    existing_files = [f for f in os.listdir(RESULT_DIR) if f.endswith('.jpg')]
    existing_labels = [f.rsplit("_", 1)[0] for f in existing_files if "_" in f]
else:
    existing_files = []
    existing_labels = []

print(f"本地已有 {len(existing_files)} 个文件")

collected = []
very_new_labels = []

for i in range(COUNT):
    result = draw()
    if isinstance(result, tuple):
        label, filename = result
        if filename in existing_files:
            print(f"图片 {filename} 已存在，跳过")
        else:
            if len(existing_labels) > 0:
                max_sim = max(SequenceMatcher(None, label, old_label).ratio() for old_label in existing_labels)
                if max_sim < 0.6:
                    print(f"!!! 极新关卡: {label} (相似度: {max_sim:.2f})")
                    very_new_labels.append(label)
            
            collected.append(label)
            existing_files.append(filename)
            existing_labels.append(label)
    elif result is False:
        break
    time.sleep(0.5)

if collected:
    print(f"\n抽到 {len(collected)} 张新图: {collected}")
    update_readme(collected)
    
    if very_new_labels:
        with open("very_new.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(very_new_labels))
        print(f"\n发现 {len(very_new_labels)} 个极新关卡，已写入 very_new.txt")
else:
    print("\n未抽到新图")