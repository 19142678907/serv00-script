import subprocess
import json
import os

# 从环境变量中获取配置信息
accounts_json = os.getenv("ACCOUNTS_JSON")
telegram_token = os.getenv("TELEGRAM_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

# 定义一个函数发送消息到Telegram
def send_telegram_message(message):
    subprocess.run([
        'curl', '-s', '-X', 'POST', f'https://api.telegram.org/bot{telegram_token}/sendMessage',
        '-d', f'chat_id={telegram_chat_id}', '-d', f'text={message}'
    ])

# 定义一个函数恢复vless服务
def recover_vless():
    accounts = json.loads(accounts_json)
    results = []

    for account in accounts:
        try:
            server = account['server']
            port = account['port']
            uuid = account['uuid']
            domain = account['domain']
            
            result = f"成功恢复 {server} 上的 vless 服务：\n"
            
            # 检查vless服务并进行恢复
            process = subprocess.run(['ssh', server, 'bash', 'vless/check_vless.sh'], capture_output=True, text=True)
            
            if process.returncode == 0:
                result += f"UUID: {uuid}\nPort: {port}\n域名: {domain}\n"
                result += f"VLESS节点信息: vless://{uuid}@{domain}:{port}?flow=&security=none&encryption=none&type=ws&host={domain}&path=/&sni=&fp=&pbk=&sid=#admin\n"
                result += "检查并恢复成功。\n"
            else:
                result += f"恢复失败，错误信息：{process.stderr}\n"
            
            results.append(result)
        
        except Exception as e:
            results.append(f"{server} 上的恢复操作失败：{str(e)}\n")

    # 发送所有结果到Telegram
    send_telegram_message("\n\n".join(results))

if __name__ == "__main__":
    recover_vless()
