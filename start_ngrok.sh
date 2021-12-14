#!/bin/bash

while true   # 无限循环
flag=`sudo ps -aux |grep "ngrok http" |grep -v "grep" |wc -l`
do
        if [[ $flag -eq 0 ]]   # 判断进程数如果等于0，则启动httpd
        then
                echo 111
                `nohup /data/data/com.termux/files/usr/bin/ngrok http --region=ap --authtoken 21wt5VZONb0oviUCLhjtHp6H7yH_4hS35h9wz8wBKf9XzjgVp --hostname=triata.ap.ngrok.io -host-header=rewrite 8080 &`   # 启动httpd
                echo "ngrok restart"
        else
                echo "ngrok is running..."
        fi
        sleep 30s  # 延迟3秒后进入下次循环
done
