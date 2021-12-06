# 算法具体实现在so函数，快手获得sig签名 rpc调用 2021-12-1  frida==15.1.1  andriod==8.1
import time
import frida
import sys
from urllib.parse import urlencode
import requests
import os

class Kuaishou(object):
    hook_code = '''
    rpc.exports = {
        getsig: function(encode_param){
            var sig = '';
            Java.perform(
                function(){
                    var CPU = Java.use('com.yxcorp.gifshow.util.CPU');
                    var currentApplication = Java.use('android.app.ActivityThread').currentApplication();
                    var context = currentApplication.getApplicationContext();
                    var b = stringToBytes(encode_param)
                    sig = CPU.getClock(context,b,27)
                }
            )
            return sig;
        }
    }
    function bytesToString(arr) {
        if(typeof arr === 'string') {
            return arr;
        }
        var str = '',
            _arr = arr;
        for(var i = 0; i < _arr.length; i++) {
            var one = _arr[i].toString(2),
                v = one.match(/^1+?(?=0)/);
            if(v && one.length == 8) {
                var bytesLength = v[0].length;
                var store = _arr[i].toString(2).slice(7 - bytesLength);
                for(var st = 1; st < bytesLength; st++) {
                    store += _arr[st + i].toString(2).slice(2);
                }
                str += String.fromCharCode(parseInt(store, 2));
                i += bytesLength - 1;
            } else {
                str += String.fromCharCode(_arr[i]);
            }
        }
        return str;
    }
    function stringToBytes(str) {
        var ch, st, re = [];
        for (var i = 0; i < str.length; i++ ) {
            ch = str.charCodeAt(i);
            st = [];
            do {
                st.push( ch & 0xFF );
                ch = ch >> 8;
            }
            while ( ch );
            re = re.concat( st.reverse() );
        }
        return re;
    }
    '''

    def hook_prepare(self,processname):
        for i in range(2):
            try:
                process = frida.get_local_device().attach(processname)
            except:
                # 杀死进程并且重启和重启frida-server
                os.system('pkill -9  "smile.gifmaker"')
                os.system('am start -n com.smile.gifmaker/com.yxcorp.gifshow.HomeActivity')
                os.system('pkill -9  "frida-server"')
                os.system('sudo /data/local/tmp/frida-server-15.1.9-android-arm64')
                time.sleep(1)
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

    def get_kuishou_sig(self,script,data={}, form_data={}):
        data.update(form_data)
        data_str = self.sort_data(data)
        sig = script.exports.getsig(data_str)
        return sig

    def on_message(self,message, data):
        if message['type'] == 'send':
            print("[*] {0}".format(message['payload']))
        else:
            print(message)

if __name__ == '__main__':
    pass
