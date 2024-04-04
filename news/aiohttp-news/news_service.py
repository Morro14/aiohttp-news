import aiohttp
import asyncio
import json

news = [{"title": "article 1", "text": "article text 1"}, {"title": "article 2", "text": "article text 2"},
        {"title": "article 3", "text": "article text 3"}]
news = json.dumps(news)


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8080/news', data={"news": news}) as resp:
            print("connected to server")
            print(resp.status)
            print(await resp.text())
    print('disconnected')


asyncio.run(main())
