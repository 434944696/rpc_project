# pdd获取anti-token参数  frida==15.1.1  andriod==8.1
import re
import time
import frida
import os


class Pdd(object):
    hook_code = ''
    with open('pinduoduo.js', 'r')as f:
        hook_code = f.read()

    def hook_prepare(self, processname):
        for i in range(2):
            try:
                process = frida.get_local_device().attach(processname)
            except:
                # 重启app，rpc服务每隔30秒检测一次没有进程就开启进程（三个sh脚本完成）
                os.system('pkill -9  "xunmeng.pinduoduo"')
                os.system('am start -n com.xunmeng.pinduoduo/com.xunmeng.pinduoduo.ui.activity.HomeActivity')
                os.system('pkill -9  "frida-server"')
                os.system('sudo /data/local/tmp/frida-server-15.1.9-android-arm64')
                time.sleep(30)
                continue
            script = process.create_script(self.hook_code)
            script.on('message', self.on_message)
            script.load()
            return script

    def getantitoken(self,script, url):
        path_url = ''.join(re.findall('.com(.*?)\?', url)).replace('/api','api')
        anti_token = script.exports.getantitoken(path_url)
        return anti_token

    def on_message(self, message, data):
        if message['type'] == 'send':
            print("[*] {0}".format(message['payload']))
        else:
            print(message)


if __name__ == '__main__':
    pass
