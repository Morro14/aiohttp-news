import aiohttp
from aiohttp import web
import asyncio
import json

news_service = []
news_update = False


async def on_shutdown(app: web.Application):
    for ws in app["sockets"]:
        await ws.close()


async def async_iter(ws, t):
    global news_update
    while True:
        await asyncio.sleep(t)
        print('ping')
        await ws.send_str('ping')
        if news_update:
            news_data = {'news': news_service[0]}
            await ws.send_json(data=news_data)
            news_update = False


async def ws_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    request.app["sockets"].append(ws)
    user_connected = await ws.receive()
    print(user_connected.data)
    for ws_ in request.app["sockets"]:
        print('sending news')
        if len(news_service) != 0:
            news_data = {'news': news_service[0]}
        else:
            news_data = 'no news yet'
        await ws.send_json(data=news_data)
        print('news sent')
        try:
            await async_iter(ws_, 3)
        except ConnectionResetError:
            print('user disconnected')
            request.app["sockets"].remove(ws)
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                print('closing')
                await ws.close()
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())
    return ws


async def post_handler(request: web.Request):
    global news_update
    data = await request.post()
    news_ = data.get("news")
    news_ = json.loads(news_)
    news_service.append(news_)
    news_update = True
    return web.Response(body="ok")


app = web.Application()
app.add_routes([web.get('/ws', ws_handler)])
app.add_routes([web.post('/news', post_handler)])

app["sockets"] = []
app.on_shutdown.append(on_shutdown)
web.run_app(app)
