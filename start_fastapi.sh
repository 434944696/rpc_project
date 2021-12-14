#!/bin/bash

while true   # 无限循环
flag=`sudo ps -aux |grep "rpc_main:app" |grep -v "grep" |wc -l`
do
        if [[ $flag -eq 0 ]]   # 判断进程数如果等于0，则启动httpd
        then
                echo 111
                `nohup /data/data/com.termux/files/usr/bin/uvicorn rpc_main:app --host '0.0.0.0' --port 8080 &`   # 启动fastapi
                echo "rpc_api restart"
        else
                echo "rpc_api is running..."
        fi
        sleep 30s  # 延迟30秒后进入下次循环
done
