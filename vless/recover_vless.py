import os
import requests
import json
from subprocess import call, DEVNULL, STDOUT, check_output

# 环境变量
ACCOUNTS_JSON = os.getenv('ACCOUNTS_JSON')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Telegram消息发送失败: {response.text}")
    else:
        print(f"Telegram消息发送成功: {message}")

def check_vless_status():
    try:
        pm2_path = check_output(["which", "pm2"]).decode().strip()
        print(f"pm2 path: {pm2_path}")
        result = call(["pm2", "status", "vless"], stdout=DEVNULL, stderr=STDOUT)
        return result == 0
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
        return False

def restart_vless():
    result = call(["pm2", "restart", "vless"], stdout=DEVNULL, stderr=STDOUT)
    return result == 0

def main():
    print(f"PATH: {os.getenv('PATH')}")
    if not check_vless_status():
        message = "VLESS 进程未运行，尝试重启..."
        send_telegram_message(message)
        if restart_vless():
            message = "VLESS 进程已成功重启。"
        else:
            message = "VLESS 进程重启失败。"
        send_telegram_message(message)
    else:
        message = "VLESS 进程正在正常运行。"
        send_telegram_message(message)

if __name__ == "__main__":
    main()
