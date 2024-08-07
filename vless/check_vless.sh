#!/bin/bash

# Function to check if pm2 is installed
check_pm2_installed() {
    if command -v pm2 &>/dev/null; then
        return 0  # pm2已安装
    else
        return 1  # pm2未安装
    fi
}

# Function to install pm2
install_pm2() {
    if ! check_pm2_installed; then
        curl -s https://raw.githubusercontent.com/k0baya/alist_repl/main/serv00/install-pm2.sh | bash
        echo "pm2安装成功。"
    else
        echo "pm2已经安装。"
    fi
}

# Function to deploy vless
deploy_vless() {
    chmod +x ./vless/check_vless.sh
    npm install --prefix ./vless
    cp -r ./vless ~/domains/$USER.serv00.net
    echo -e "\033[0;32m ..."
    echo -e "请执行以下脚本:\033[0;32mcd ~/domains/$USER.serv00.net/vless && ./check_vless.sh -p <端口号>\033[0m"
}

# Main function
main() {
    echo "正在安装pm2..."
    install_pm2
    echo "正在部署vless到指定目录..."
    deploy_vless
}

# 执行主函数
main "$@"
