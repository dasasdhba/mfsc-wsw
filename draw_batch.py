import os
import time
import requests
import base64
import hashlib

API_URL = "https://zh.wsw233.com/api/tools/mfsc_special/draw"
RESULT_DIR = "result"
COUNT = 1000

os.makedirs(RESULT_DIR, exist_ok=True)

def draw():
    resp = requests.post(API_URL)
    data = resp.json()
    
    if data.get("code") not in [0, 1]:
        print(f"抽取失败: {data.get('message', '未知错误')}")
        return None
    
    code = data["code"]
    image_data = data["image"]
    is_new = code == 0
    
    if is_new:
        img_bytes = base64.b64decode(image_data)
        img_hash = hashlib.md5(img_bytes).hexdigest()[:8]
        filename = f"new_{img_hash}.png"
        filepath = os.path.join(RESULT_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(img_bytes)
        return True
    else:
        return False

print(f"开始抽取 {COUNT} 次...")
new_count = 0
old_count = 0

for i in range(COUNT):
    result = draw()
    if result is True:
        new_count += 1
    elif result is False:
        old_count += 1
    
    print(f"进度: {i+1}/{COUNT} (new: {new_count}, old: {old_count})")
    time.sleep(0.5)

print(f"\n完成！共抽取 {COUNT} 次")
print(f"有效抽取 (is_new=True): {new_count}")
print(f"无效抽取 (is_new=False): {old_count}")