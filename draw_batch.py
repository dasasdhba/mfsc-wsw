import os
import time
import requests
import base64
import hashlib
from datetime import datetime

API_URL = "https://zh.wsw233.com/api/tools/mfsc_special/draw"
RESULT_DIR = "result"
COUNT = 10

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
        print(f"有效抽取: {filename}")
        return True
    else:
        print("遇到无效抽取，停止")
        return False

print(f"[{datetime.now()}] 开始抽取最多 {COUNT} 次，遇到 false 停止...")
new_count = 0
found_new = False

for i in range(COUNT):
    result = draw()
    if result is True:
        new_count += 1
        found_new = True
    elif result is False:
        break
    
    time.sleep(0.5)

if found_new:
    print(f"\n抽到 {new_count} 张新图，标记为失败以发送通知")
    raise SystemExit(1)

print(f"\n完成！有效抽取: {new_count} 次")