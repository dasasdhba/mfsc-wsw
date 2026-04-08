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

SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")
GITHUB_TOKEN = os.getenv("MY_TOKEN")
OWNER = os.getenv("OWNER")
REPO = os.getenv("REPO")

os.makedirs(RESULT_DIR, exist_ok=True)
def ocr_extract_label(img_path, max_retries=3):
    """使用硅基流动 DeepSeek OCR"""
    with open(img_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    
    from PIL import Image
    img = Image.open(img_path)
    w, h = img.size
    left = 0
    top = int(h * 0.8)
    right = int(w * 0.7)
    bottom = h
    crop = img.crop((left, top, right, bottom))
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
    headers = {
        "Authorization": f"Bearer {SILICONFLOW_API_KEY}",
        "Content-Type": "application/json"
    }
    
    for attempt in range(max_retries):
        resp = requests.post(url, json=payload, headers=headers)
        
        if resp.status_code == 429 or "RPM limit" in resp.text:
            wait_time = 15 * (attempt + 1)
            print(f"  OCR限速触发，等待 {wait_time} 秒...")
            time.sleep(wait_time)
            continue
        
        if resp.ok:
            result = resp.json()
            text = result["choices"][0]["message"]["content"]
            text = text.strip()
            text = text.replace('\n', '-').replace('\r', '-')
            text = text.replace(' -', '-').replace('- ', '-')
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
        print(f"抽取失败: {data.get('message', '未知错误')}")
        return None
    
    code = data["code"]
    image_data = data["image"]
    is_new = code == 0
    
    if is_new:
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
        
        print(f"有效抽取: {filename} (标签: {label})")
        return (label, img_hash, filename)
    else:
        print("遇到无效抽取，停止")
        return False
def get_existing_files():
    if not GITHUB_TOKEN:
        return []
    from github import Github
    g = Github(GITHUB_TOKEN)
    try:
        repo = g.get_repo(f"{OWNER}/{REPO}")
        contents = repo.get_contents("result")
        return [c.name for c in contents]
    except:
        return []
def commit_to_repo(new_images):
    if not GITHUB_TOKEN:
        print("未配置 GITHUB_TOKEN，跳过提交")
        return
    
    from github import Github
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(f"{OWNER}/{REPO}")
    
    # 直接从本地读取 README
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as f:
            readme_content = f.read()
    else:
        readme_content = ""
    
    new_lines = [f"- {img[0]}" for img in new_images]
    new_content = readme_content + "\n" + "\n".join(new_lines)
    
    updates = []
    for label, img_hash, filename in new_images:
        filepath = os.path.join(RESULT_DIR, filename)
        with open(filepath, "rb") as f:
            content = f.read()
        content_b64 = base64.b64encode(content).decode('utf-8')
        updates.append({
            "path": f"result/{filename}",
            "content": content_b64,
            "message": f"Add {filename}"
        })
    
    updates = []
    for label, img_hash, filename in new_images:
        filepath = os.path.join(RESULT_DIR, filename)
        with open(filepath, "rb") as f:
            content = f.read()
        content_b64 = base64.b64encode(content).decode('utf-8')
        updates.append({
            "path": f"result/{filename}",
            "content": content_b64,
            "message": f"Add {filename}"
        })
    
    # README 最后提交
    updates.append({
        "path": "README.md",
        "content": base64.b64encode(new_content.encode('utf-8')).decode('utf-8'),
        "message": "Update README"
    })
    
    try:
        # 先提交图片文件
        for update in updates[:-1]:
            try:
                existing = repo.get_contents(update["path"])
                sha = existing.sha if existing else None
            except Exception:
                sha = None
            
            if sha:
                repo.update_file(path=update["path"], message=update["message"], content=update["content"], sha=sha, branch="main")
            else:
                repo.create_file(path=update["path"], message=update["message"], content=update["content"], branch="main")
        
        # 最后提交 README（需要获取最新 sha）
        readme_update = updates[-1]
        try:
            existing = repo.get_contents("README.md")
            sha = existing.sha if existing else None
        except Exception:
            sha = None
        
        if sha:
            repo.update_file(path=readme_update["path"], message=readme_update["message"], content=readme_update["content"], sha=sha, branch="main")
        else:
            repo.create_file(path=readme_update["path"], message=readme_update["message"], content=readme_update["content"], branch="main")
        
        print(f"已提交 {len(new_images)} 个新文件")
    except Exception as e:
        print(f"提交失败: {e}")
        raise

print(f"[{datetime.now()}] 开始抽取最多 {COUNT} 次，遇到 false 停止...")

existing_files = get_existing_files()
collected = []
very_new_labels = []

for i in range(COUNT):
    result = draw()
    if isinstance(result, tuple):
        label, img_hash, filename = result
        
        # 检查是否完全相同
        if filename in existing_files:
            print(f"图片 {filename} 已存在，跳过")
        else:
            # 检查与既有文件的相似度
            if len(existing_files) > 5:
                existing_labels = [f.rsplit("_", 1)[0] for f in existing_files if "_" in f]
                max_sim = max(SequenceMatcher(None, label, old_label).ratio() for old_label in existing_labels)
                
                if max_sim < 0.3:
                    print(f"!!! 极新关卡: {label} (相似度: {max_sim:.2f})")
                    very_new_labels.append(label)
            
            collected.append(result)
            existing_files.append(filename)
    elif result is False:
        break
    
    time.sleep(0.5)

if collected:
    print(f"\n抽到 {len(collected)} 张新图")
    commit_to_repo(collected)
    
    # 如果有极新关卡，触发通知
    if very_new_labels:
        print(f"\n发现 {len(very_new_labels)} 个极新关卡: {very_new_labels}")
        raise SystemExit(1)
else:
    print(f"\n完成！有效抽取: 0 次")
