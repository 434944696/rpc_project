# 启动fastApi服务 uvicorn rpc_main:app --host '0.0.0.0' --port 8080 --reload
from fastapi import FastAPI
from pydantic import BaseModel
from rpc_kuaishou_sig import Kuaishou
from rpc_douyin_gorgon import DouYin
import json


class Item(BaseModel):
    data: str
    formdata: str
    processname: str


class DYItem(BaseModel):
    timestamp: int
    salt: str
    process_name: str


app = FastAPI()

kuaishou = Kuaishou()
script = kuaishou.hook_prepare('快手')


@app.post("/kuaishou/get_sig/")
async def kuaishou_get_sig(item: Item):
    data = json.loads(item.data)
    form_data = json.loads(item.formdata)
    processname = item.processname
    sig = kuaishou.get_kuishou_sig(script,data=data, form_data=form_data)
    return sig


@app.post("/douyin/get_gorgon/")
async def kuaishou_get_sig(item: DYItem):
    douyin = DouYin()
    process_name = item.process_name
    dy_script = douyin.hook_prepare(process_name=process_name)
    timestamp = item.timestamp
    salt = item.salt
    gorgon = dy_script.get_douyin_gorgon(dy_script, timestamp=timestamp, salt=salt)
    return gorgon

