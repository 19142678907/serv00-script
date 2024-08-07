#!/bin/bash

# ANSI颜色码
GREEN='\033[0;32m'
NC='\033[0m'  # 恢复默认颜色

# 输出绿色的 "YI XIU"
output_yi_xiu() {
    echo -e "${GREEN}YI XIU${NC}"
}

# Function to generate a UUID
generate_uuid() {
    for i in {1..3}; do
        uuid=$(uuidgen)
        if [[ -n "$uuid" ]]; then
            echo "$uuid"
            return
        fi
    done
}

# Function to save config.json
save_config() {
    local port=$1
    if [[ ! -f ~/domains/$USER.serv00.net/vless/config.json ]]; then
        uuid=$(generate_uuid)
        cat <<EOL > ~/domains/$USER.serv00.net/vless/config.json
{
    "uuid": "$uuid",
    "port": $port
}
EOL
        echo "生成config.json文件。"
    else
        jq --arg port "$port" '.port = ($port | tonumber)' ~/domains/$USER.serv00.net/vless/config.json > ~/domains/$USER.serv00.net/vless/config_tmp.json && mv ~/domains/$USER.serv00.net/vless/config_tmp.json ~/domains/$USER.serv00.net/vless/config.json
        echo "config.json文件已存在，端口号已更新。"
    fi
}

# Function to deploy vless
deploy_vless() {
    local port=${1:-3000}  # Default port is 3000 if not provided
    save_config "$port"
    npm install
    ~/.npm-global/bin/pm2 start ~/domains/$USER.serv00.net/vless/app.js --name vless
    ~/.npm-global/bin/pm2 save
    output_yi_xiu
    echo -e "端口号: ${GREEN}${port}${NC}"
    echo -e "UUID: ${GREEN}${uuid}${NC}"
    echo -e "域名: ${GREEN}$USER.serv00.net${NC}"
}

# 启动pm2 vless进程
start_pm2_vless_process() {
    echo "正在启动pm2 vless进程..."
    ~/.npm-global/bin/pm2 start ~/domains/$USER.serv00.net/vless/app.js --name vless
    echo -e "${GREEN}pm2 vless进程已启动。${NC}"
}

# 检查vless的状态
check_vless_status() {
    status=$(pm2 status vless | grep -w 'vless' | awk '{print $18}')
    if [[ "$status" == "online" ]]; then
        echo "vless进程正在运行。"
    else
        echo "vless进程未运行或已停止，正在重启..."
        pm2 restart vless
        echo -e "${GREEN}vless进程已重启。${NC}"
    }
}

# 检查是否有pm2 vless快照
check_pm2_vless_snapshot() {
    if [[ -f ~/.pm2/dump.pm2 ]]; then
        echo "检测到pm2 vless快照，正在恢复..."
        pm2 resurrect
        echo -e "${GREEN}pm2 vless快照已恢复。${NC}"
        check_vless_status
    else
        echo "未检测到pm2 vless快照，启动vless进程..."
        start_pm2_vless_process
    }
}

# 检查pm2 vless的状态
check_pm2_vless_status() {
    pm2 describe vless &>/dev/null
    if [[ $? -eq 0 ]]; then
        check_vless_status
    else
        echo "未找到pm2 vless进程，检查是否有快照..."
        check_pm2_vless_snapshot
    }
}

# 主函数
main() {
    local port=3000  # Default port
    port_provided=false  # Flag to check if port is provided

    while getopts ":p:" opt; do
        case $opt in
            p)
                port=$OPTARG
                port_provided=true
                ;;
            *)
                echo "无效参数"; exit 1 ;;
        esac
    done
    shift $((OPTIND -1))

    if [ "$port_provided" = true ]; then
        echo "正在安装vless..."
        deploy_vless "$port"
    else
        echo "没有提供-p参数，跳过vless安装。"
        if [[ -f config.json ]]; then
            uuid=$(jq -r '.uuid' config.json)
            port=$(jq -r '.port' config.json)
            echo -e "UUID: ${uuid}"
            echo -e "Port: ${port}"
            echo -e "域名: $USER.serv00.net"
            echo -e "VLESS节点信息: vless://${uuid}@$USER.serv00.net:${port}?flow=&security=none&encryption=none&type=ws&host=$USER.serv00.net&path=%2F&serviceName=&sni=$USER.serv00.net"
        fi
    fi
}

main "$@"
