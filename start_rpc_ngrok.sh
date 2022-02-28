#!/bin/bash

flag2=`sudo ps -aux |grep "ngrok http" |grep -v "grep" |wc -l`
if [ $flag2 -eq 0 ]   # 判断进程数如果等于0，等于则启动
then
        `su & nohup /data/data/com.termux/files/usr/bin/ngrok http --region=ap --authtoken 21wt5VZONb0oviUCLhjtHp6H7yH_4hS35h9wz8wBKf9XzjgVp --hostname=triata.ap.ngrok.io -host-header=rewrite 8080 >ngrok.log 2>&1 &`   # 启动httpd
        echo "ngrok restart"
else
        echo "ngrok is running..."
fi

flag=`sudo ps -aux |grep "rpc_main:app" |grep -v "grep" |wc -l`
if [ $flag -eq 0 ]  # 判断进程数如果等于0，等于则启动
then
        `su & nohup /data/data/com.termux/files/usr/bin/uvicorn rpc_main:app --host '0.0.0.0' --port 8080 >rpc.log 2>&1 &`   # 启动fastapi
        echo "rpc_api restart"
else
        echo "rpc_api is running..."
fi



