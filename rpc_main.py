# 启动fastApi服务 uvicorn rpc_main:app --host '0.0.0.0' --port 8080 --reload
# 手机 /data/data/com.termux/files/usr/bin/uvicorn rpc_main:app --host '0.0.0.0' --port 8080
from pydantic import BaseModel
from rpc_kuaishou_sig import Kuaishou
from rpc_douyin_gorgon import DouYin
from rpc_pinduoduo_anti_token import Pdd
import json
from fastapi import FastAPI
import frida
from routes.beike import beike_route
import uvicorn


class Item(BaseModel):
    data: str
    formdata: str
    processname: str


class KSItem2(BaseModel):
    sig: str
    url: str
    processname: str


class DYItem(BaseModel):
    timestamp: int
    salt: str
    processname: str


class PDItem(BaseModel):
    url: str
    processname: str


app = FastAPI()
app.router.include_router(beike_route, prefix='/beike')
kuaishou = Kuaishou()
douyin = DouYin()
pdd = Pdd()
kuaishou_script_is_exist = False
kuaishou_script = ''
douyin_script_is_exist = False
douyin_script = ''
pinduoduo_script_is_exist = False
pinduoduo_script = ''


@app.post("/kuaishou/get_sig/")
async def kuaishou_get_sig(item: Item):
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


@app.post("/kuaishou/get_sig3/")
async def kuaishou_get_sig3(item: KSItem2):
    url = item.url
    sig = item.sig
    processname = item.processname
    global kuaishou_script_is_exist
    if not kuaishou_script_is_exist:
        global kuaishou_script
        kuaishou_script = kuaishou.hook_prepare(processname)
        kuaishou_script_is_exist = True
    try:
        sig3 = kuaishou.get_kuishou_sig3(kuaishou_script, sig, url)
    except frida.InvalidOperationError:
        kuaishou_script = kuaishou.hook_prepare(processname)
        kuaishou_script_is_exist = True
        sig3 = kuaishou.get_kuishou_sig3(kuaishou_script, sig, url)
    return sig3


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
    gorgon = douyin.get_douyin_gorgon(douyin_script, timestamp=timestamp, salt=salt)
    return gorgon


@app.post("/pinduoduo/get_antitoken/")
async def pinduoduo_get_antitoken(item: PDItem):
    url = item.url
    processname = item.processname
    global pinduoduo_script_is_exist
    if not pinduoduo_script_is_exist:
        global pinduoduo_script
        pinduoduo_script = pdd.hook_prepare(processname)
        pinduoduo_script_is_exist = True
    try:
        antitoken = pdd.getantitoken(pinduoduo_script, url)
    except frida.InvalidOperationError:
        pinduoduo_script = pdd.hook_prepare(processname)
        pinduoduo_script_is_exist = True
        antitoken = pdd.getantitoken(pinduoduo_script, url)
    return antitoken


if __name__ == '__main__':
    uvicorn.run(app='rpc_main:app', host='0.0.0.0', port=8080, reload=True)
