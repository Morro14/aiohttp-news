import aiohttp
import asyncio
import json


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('http://localhost:8080/ws') as ws:
            print("connected to server")


            await ws.send_str('user connected')
            async for msg in ws:

                if msg.type == aiohttp.WSMsgType.TEXT:
                    try:
                        data = json.loads(msg.data)
                    except json.decoder.JSONDecodeError:
                        pass

                    if isinstance(data, dict):
                        print('New articles!')
                        for n in data["news"]:
                            print(n["text"])
                        data = None
                    # except json.decoder.JSONDecodeError or TypeError:
                    else:
                        print(msg.data)

asyncio.run(main())
