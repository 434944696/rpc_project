#!/bin/bash
#得到对应服务的进程号
my_array=()
my_array[0]="ngrok http"
my_array[1]="rpc_main:app"
my_array[2]="frida-serverp"
for i in ${my_array[@]}; do
    echo $i;
  str=`sudo ps -ef | grep $i | grep -v "grep"|awk '{print $2}'`
  #获取进程所在的目录
  pwd=`sudo ls -l /proc/${str} | grep "cwd ->" | grep -v "grep" | awk '{print $NF}'`
  echo "进程目录是："$pwd
  sudo kill -9 $str
  if [ "$?" -eq 0 ]; then
                  echo "killed pid is "$str
                      echo "kill success"
              else
                          echo "kill failed"
                  fi


flag2=`sudo ps -aux |grep "ngrok http" |grep -v "grep" |wc -l`
if [ $flag2 -eq 0 ]   # 判断进程数如果等于0，等于则启动
then
        `su & nohup /data/data/com.termux/files/usr/bin/ngrok http --region=ap --authtoken 21wt5VZONb0oviUCLhjtHp6H7yH_4hS35h9wz8wBKf9XzjgVp --hostname=triata.ap.ngrok.io -host-header=rewrite 8080 >ngrok.log 2>&1 &`   # 启动httpd,只输出ngrok.log不输出nohup.log
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

flag3=`sudo ps -aux |grep "frida-server" |grep -v "grep" |wc -l`
if [ $flag3 -eq 0 ]  # 判断进程数如果等于0，等于则启动
then
        `su & nohup /data/local/tmp/frida-server-15.1.9-android-arm64 >frida_server.log 2>&1 &`
        echo "frida-server restart"
else
        echo "frida-server is running..."
fi


