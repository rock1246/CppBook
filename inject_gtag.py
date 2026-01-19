import os
import re

# ================= 配置設定 =================
# 1. 指定你的網站根目錄路徑
target_directory = r'G:\test\tmp\CppBook'

# 2. 你的 Google Analytics 程式碼
gtag_id = "G-1MJWMS1CQD"
gtag_code = f"""
<script async src="https://www.googletagmanager.com/gtag/js?id={gtag_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{gtag_id}');
</script>
"""
# ===========================================

def inject_gtag(directory):
    # 遍歷資料夾及其所有子資料夾
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith('.html'):
                file_path = os.path.join(root, filename)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 檢查是否已經安裝過，避免重複插入
                if gtag_id in content:
                    print(f"跳過: {file_path} (已存在 gtag)")
                    continue

                # 在 <head> 標籤後插入程式碼 (忽略大小寫)
                # 使用正則表達式確保能捕捉到 <head> 或 <HEAD>
                new_content = re.sub(r'(<head.*?>)', r'\1' + gtag_code, content, flags=re.IGNORECASE, count=1)

                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"成功更新: {file_path}")
                else:
                    print(f"警告: 在 {file_path} 中找不到 <head> 標籤")

if __name__ == "__main__":
    if os.path.exists(target_directory):
        inject_gtag(target_directory)
        print("\n--- 處理完成 ---")
    else:
        print(f"錯誤: 找不到路徑 '{target_directory}'")
