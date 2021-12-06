# 算法具体实现在so函数，抖音获得gorgon rpc调用 2021-12-6  frida==15.1.1  andriod==8.1
import time
import frida
import os


class DouYin(object):
    hook_code = """
    rpc.exports = {
        getgorgon: function(timestamp, salt) {
            var gorgon = ""
            Java.perform(function() {
                var a = Java.use("com.ss.a.b.a")
                var ka = Java.use("com.ss.sys.ces.a")
                gorgon = a.a(ka.leviathan(-1, timestamp, a.a(salt)))
            })
            return gorgon
        }
    }
    """
    process_name = '抖音短视频'       # 抖音版本13.0.0

    def hook_prepare(self, process_name):
        for i in range(2):
            try:
                process = frida.get_local_device().attach(process_name)
            except:
                # 杀死进程并且重启和重启frida-server
                os.system('pkill -9  "aweme"')
                os.system('am start -n com.ss.android.ugc.aweme/.main.MainActivity')
                os.system('pkill -9  "frida-server"')
                os.system('sudo /data/local/tmp/frida-server-15.1.9-android-arm64')
                time.sleep(1)
                continue
            script = process.create_script(self.hook_code)
            script.on('message', self.on_message)
            script.load()
            return script

    @staticmethod
    def get_douyin_gorgon(script, timestamp, salt):
        gorgon = script.exports.getgorgon(int(timestamp), salt)
        return gorgon

    @staticmethod
    def on_message(message, data):
        if message['type'] == 'send':
            print("[*] {0}".format(message['payload']))
        else:
            print(message)


if __name__ == '__main__':
    pass




