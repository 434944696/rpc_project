import os
import frida
import requests


def robust_frida(func):
    def wrapper(self=None, *args):
        error_msg = ""
        for _ in range(3):
            try:
                return func(self, *args)
            except (frida.InvalidOperationError, frida.ProcessNotFoundError, frida.TransportError) as e:
                error_msg = e
                self.restart_app()
                self.attach_script()
        self.feishu_alert(f"重启{self.app_name}app, 未能解决问题 报错信息: {error_msg}")
    return wrapper


class Beike:
    _instance: object
    app_name: str = "贝壳找房"
    script: frida.core.Script
    activity_name: str = "com.lianjia.beike/com.lianjia.activity.MainActivity"
    feishu_webhook = "https://open.feishu.cn/open-apis/bot/v2/hook/94ad8956-918a-4086-9a4a-660ef7b540d8"

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance: Beike = super().__new__(cls)
            cls._instance.restart_app()
            cls._instance.attach_script()
        return cls._instance

    def feishu_alert(self, msg: str):
        data = {"msg_type": "text", "content": {"text": msg}}
        requests.post(self.feishu_webhook, json=data)

    @robust_frida
    def restart_app(self):
        os.system(f'am start -S -n {self.activity_name}')

    @robust_frida
    def attach_script(self):
        script = """
        rpc.exports = {
            getSign(params, access_key_id, timestamp) {
                let sign = '';
                Java.perform(() => {
                    const env = Java.use('com.ke.infrastructure.app.signature.algorithm.V1SignAlgorithm');
                    timestamp = Java.use('java.lang.Long').$new(timestamp);
                    sign = env.$new().sign(params, access_key_id, timestamp);
                });
                return sign[0];
                }
            };"""
        process = frida.get_local_device().attach(self.app_name)
        self.script = process.create_script(script)
        self.script.load()

    @robust_frida
    def get_sign(self, params: str, access_key_id: str, timestamp: int):
        return self.script.exports.get_sign(params, access_key_id, timestamp)
