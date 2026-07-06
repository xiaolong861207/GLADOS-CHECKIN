import requests
import os
import sys

def main():
    # 从环境变量获取 Cookie
    cookie = os.environ.get('GLADOS_COOKIE')
    if not cookie:
        print("❌ 错误：未找到 GLADOS_COOKIE，请在 GitHub Secrets 中设置")
        sys.exit(1)

    headers = {
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Origin': 'https://glados.network',
        'Referer': 'https://glados.network/'
    }

    # 尝试通用的签到接口
    urls = [
        'https://glados.network/api/user/checkin',
        'https://glados.rocks/api/user/checkin'
    ]

    success = False
    for url in urls:
        try:
            resp = requests.post(url, headers=headers, timeout=10)
            data = resp.json()
            # ✅ 修正：Glados 接口返回 code=1 表示签到成功
            if data.get('code') == 1:
                change = data.get('change', 0)
                balance = data.get('balance', 0)
                message = data.get('message', '')
                print(f"✅ 签到成功！增加 {change} 积分，当前总积分 {balance}，消息：{message}")
                success = True
                break
            else:
                print(f"⚠️ 尝试 {url} 返回：{data}")
        except Exception as e:
            print(f"❌ 请求 {url} 失败：{e}")

    if not success:
        print("❌ 所有签到接口均失败，请检查 Cookie 是否过期")
        sys.exit(1)

if __name__ == "__main__":
    main()
