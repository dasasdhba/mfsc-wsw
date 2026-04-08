import os
import time
import requests
import base64
import hashlib
from datetime import datetime
from PIL import Image

API_URL = "https://zh.wsw233.com/api/tools/mfsc_special/draw"
RESULT_DIR = "result"
COUNT = 10
README_FILE = "README.md"

SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")

os.makedirs(RESULT_DIR, exist_ok=True)

def ocr_extract_label(img_path, max_retries=3):
    with open(img_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    
    img = Image.open(img_path)
    w, h = img.size
    crop = img.crop((0, int(h*0.8), int(w*0.7), h))
    crop_path = os.path.join(RESULT_DIR, "temp_crop.jpg")
    crop.save(crop_path, "JPEG")
    
    with open(crop_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    os.remove(crop_path)
    
    url = "https://api.siliconflow.cn/v1/chat/completions"
    payload = {
        "model": "Qwen/Qwen2-VL-72B-Instruct",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "请识别图片左下角区域的所有文字内容。包括关卡名称、难度评价(难度:xx难度)、WSW的编号等所有信息。直接返回识别的文字，不要做任何解释。"},
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
    
    for label in new_items:
        line = f"- {label}"
        if line not in content:
            content += line + "\n"
    
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"已更新 README.md")

print(f"[{datetime.now()}] 本地测试开始，抽取最多 {COUNT} 次...")

collected = []
existing = set(os.listdir(RESULT_DIR))

for i in range(COUNT):
    result = draw()
    if isinstance(result, tuple):
        label, filename = result
        if filename not in existing:
            collected.append(label)
            existing.add(filename)
    elif result is False:
        break
    time.sleep(0.5)

if collected:
    print(f"\n抽到 {len(collected)} 张新图: {collected}")
    update_readme(collected)
    print("\n结果:")
    print(f"  图片保存在: {RESULT_DIR}/")
    print(f"  README 已更新")
else:
    print("\n未抽到新图")

print("\n本地测试完成!")
