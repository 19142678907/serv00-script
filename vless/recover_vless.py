import os
import subprocess
import requests

def recover_vless():
    try:
        subprocess.run(['bash', 'vless/check_vless.sh'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")
        raise

def send_telegram_message(token, chat_id, message):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, data=data)
    response.raise_for_status()

if __name__ == '__main__':
    recover_vless()
    
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    telegram_chat_id = os.getenv
