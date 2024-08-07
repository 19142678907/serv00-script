import os
import requests
import subprocess

def send_telegram_message(message):
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {
        'chat_id': telegram_chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to send message: {response.text}")

def recover_vless():
    try:
        result = subprocess.run(['bash', 'vless/check_vless.sh'], check=True, text=True, capture_output=True)
        output = result.stdout
        message = f"serv00-vless 恢复操作结果：\n\n{output}"
        send_telegram_message(message)
    except subprocess.CalledProcessError as e:
        send_telegram_message(f"VLESS 服务恢复失败：{e.output}")

if __name__ == "__main__":
    recover_vless()
