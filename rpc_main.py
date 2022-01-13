# 启动fastApi服务 uvicorn rpc_main:app --host '0.0.0.0' --port 8080 --reload
# 手机 /data/data/com.termux/files/usr/bin/uvicorn rpc_main:app --host '0.0.0.0' --port 8080
from pydantic import BaseModel
from rpc_kuaishou_sig import Kuaishou
from rpc_douyin_gorgon import DouYin
import json
from fastapi import FastAPI
import frida


class KYItem(BaseModel):
    data: str
    formdata: str
    processname: str


class DYItem(BaseModel):
    timestamp: int
    salt: str
    processname: str


app = FastAPI()
kuaishou = Kuaishou()
douyin = DouYin()

kuaishou_script_is_exist = False
kuaishou_script = ''
douyin_script_is_exist = False
douyin_script = ''


@app.post("/kuaishou/get_sig/")
async def kuaishou_get_sig(item: KYItem):
    data = json.loads(item.data)
    form_data = json.loads(item.formdata)
    processname = item.processname
    global kuaishou_script_is_exist
    if not kuaishou_script_is_exist:
        global kuaishou_script
        kuaishou_script = kuaishou.hook_prepare(processname)
        kuaishou_script_is_exist = True
    try:
        sig = kuaishou.get_kuishou_sig(kuaishou_script, data=data, form_data=form_data)
    except frida.InvalidOperationError:
        kuaishou_script = kuaishou.hook_prepare(processname)
        kuaishou_script_is_exist = True
        sig = kuaishou.get_kuishou_sig(kuaishou_script, data=data, form_data=form_data)
    return sig


@app.post("/douyin/get_gorgon/")
async def douyin_get_gorgon(item: DYItem):
    timestamp = item.timestamp
    salt = item.salt
    processname = item.processname
    global douyin_script_is_exist
    if not douyin_script_is_exist:
        global douyin_script
        douyin_script = douyin.hook_prepare(processname)
        douyin_script_is_exist = True
    try:
        gorgon = douyin.get_douyin_gorgon(douyin_script, timestamp=timestamp, salt=salt)
    except frida.InvalidOperationError:
        douyin_script = douyin.hook_prepare(processname)
        douyin_script_is_exist = True
        gorgon = douyin.get_douyin_gorgon(douyin_script, timestamp=timestamp, salt=salt)
    return gorgon
