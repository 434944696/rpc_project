#! /bin/sh

proc_name="rpc_main:app"        #进程名

proc_num()                      #查询进程数量
{   su
    num=$(ps -ef | grep $proc_name | grep -v grep | wc -l)
    return $num
}

proc_num
number=$?                       #获取进程数量
if [ $number -eq 0 ]            #如果进程数量为0
then                            #重新启动服务器，或者扩展其它内容。

    cd /data/data/com.termux/files/home/rpc_project
    /data/data/com.termux/files/usr/bin/ngrok http --region=ap --authtoken 21wt5VZONb0oviUCLhjtHp6H7yH_4hS35h9wz8wBKf9XzjgVp --hostname=triata.ap.ngrok.io -host-header=rewrite 8080 &

fi