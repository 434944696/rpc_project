from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from rpc_beike_signature import Beike


beike_route = APIRouter()


class BeikeSignatureParams(BaseModel):
    params: str
    timestamp: int
    access_key_id: str


@beike_route.post('/get_signature')
def get_signature(item: BeikeSignatureParams):
    signature = Beike().get_sign(item.params, item.access_key_id, item.timestamp)
    if signature:
        return JSONResponse(status_code=200, content={'code': 200, 'data': signature})
