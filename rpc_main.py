# 启动fastApi服务 uvicorn rpc_main:app --host '0.0.0.0' --port 8080 --reload
from fastapi import FastAPI
from pydantic import BaseModel
from rpc_kuaishou_sig import Kuaishou
import json


class Item(BaseModel):
    data: str
    formdata: str
    processname: str


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

