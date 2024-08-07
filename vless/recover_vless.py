import os
import subprocess
import requests

def recover_vless():
    subprocess.run(['bash', 'vless/check_vless.sh'], check=True)

def send_telegram_message(token, chat_id, message):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {'chat_id': chat_id, 'text': message}
    requests.post(url, data=data)

if __name__ == '__main__':
    recover_vless()
    
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    message = 'Vless服务已恢复。'
    
    send_telegram_message(telegram_token, telegram_chat_id, message)
