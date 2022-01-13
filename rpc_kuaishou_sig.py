# 算法具体实现在so函数，快手获得sig签名 rpc调用 2021-12-1  frida==15.1.1  andriod==8.1
import time
import frida
import sys
from urllib.parse import urlencode
import requests
import os


class Kuaishou(object):
    hook_code = ''
    with open('kuaishou.js', 'r')as f:
        hook_code = f.read()

    def hook_prepare(self, processname):
        for i in range(2):
            try:
                process = frida.get_local_device().attach(processname)
            except:
                # 重启app，rpc服务每隔30秒检测一次没有进程就开启进程（三个sh脚本完成）
                os.system('pkill -9  "smile.gifmaker"')
                os.system('am start -n com.smile.gifmaker/com.yxcorp.gifshow.HomeActivity')
                os.system('pkill -9  "frida-server"')
                os.system('sudo /data/local/tmp/frida-server-15.1.9-android-arm64')
                time.sleep(10)
                continue
            script = process.create_script(self.hook_code)
            script.on('message', self.on_message)
            script.load()
            return script

    # 将字典的键值进行排序后返回字符串
    def sort_data(self, data):
        if isinstance(data, dict):
            sort_keys = sorted(data.keys())
            result = ''
            for key in sort_keys:
                result += f"{key}={data[key]}"
            return result
        else:
            raise Exception('传入的参数必须为字典')

    def get_kuishou_sig(self, script, data={}, form_data={}):
        data.update(form_data)
        data_str = self.sort_data(data)
        sig = script.exports.getsig(data_str)
        return sig

    def on_message(self, message, data):
        if message['type'] == 'send':
            print("[*] {0}".format(message['payload']))
        else:
            print(message)


if __name__ == '__main__':
    pass
