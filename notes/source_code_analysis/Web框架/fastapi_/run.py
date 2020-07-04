"""
pip install fastapi
pip install uvicorn  # 可通过 ASGI 协议启动服务, ASGI 在 WSGI 的基础上增加异步的支持, 如 websocket

"""

from fastapi import FastAPI

app = FastAPI()


# @app.get('/')
# def home():
#     return {'data': 'At home.'}


@app.get('/')
async def home():
    return {'data': 'At home.'}

