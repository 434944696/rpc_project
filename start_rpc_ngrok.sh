#!/bin/bash
#得到对应服务的进程号
str1=`sudo ps -ef | grep "ngrok http" | grep -v "grep"|awk '{print $2}'`
str2=`sudo ps -ef | grep "rpc_main:app" | grep -v "grep"|awk '{print $2}'`
str3=`sudo ps -ef | grep "frida-server" | grep -v "grep"|awk '{print $2}'`
#获取进程所在的目录
pwd1=`sudo ls -l /proc/${str1} | grep "cwd ->" | grep -v "grep" | awk '{print $NF}'`
pwd2=`sudo ls -l /proc/${str2} | grep "cwd ->" | grep -v "grep" | awk '{print $NF}'`
pwd3=`sudo ls -l /proc/${str3} | grep "cwd ->" | grep -v "grep" | awk '{print $NF}'`
echo "进程目录是："$pwd1
echo "进程目录是："$pwd2
echo "进程目录是："$pwd3
sudo kill -9 $str1
sudo kill -9 $str2
sudo kill -9 $str3



flag2=`sudo ps -aux |grep "ngrok http" |grep -v "grep" |wc -l`
if [ $flag2 -eq 0 ]   # 判断进程数如果等于0，等于则启动
then
        echo "ngrok restart"
else
        echo "ngrok is running..."
fi

flag=`sudo ps -aux |grep "rpc_main:app" |grep -v "grep" |wc -l`
if [ $flag -eq 0 ]  # 判断进程数如果等于0，等于则启动
then        `su & nohup /data/data/com.termux/files/usr/bin/ngrok http --region=ap --authtoken 21wt5VZONb0oviUCLhjtHp6H7yH_4hS35h9wz8wBKf9XzjgVp --hostname=triata.ap.ngrok.io -host-header=rewrite 8080 >ngrok.log 2>&1 &`   # 启动httpd,只输出ngrok.log不输出nohup.log

        `su & nohup /data/data/com.termux/files/usr/bin/uvicorn rpc_main:app --host '0.0.0.0' --port 8080 >rpc.log 2>&1 &`   # 启动fastapi
        echo "rpc_api restart"
else
        echo "rpc_api is running..."
fi

flag3=`sudo ps -aux |grep "frida-server" |grep -v "grep" |wc -l`
if [ $flag3 -eq 0 ]  # 判断进程数如果等于0，等于则启动
then
        `su & nohup /data/local/tmp/frida-server-15.1.9-android-arm64 >frida_server.log 2>&1 &`
        echo "frida-server restart"
else
        echo "frida-server is running..."
fi


