import aiohttp
import asyncio
import os
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv('API_URL')

async def pull(tag: str) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{API_URL}/pull', json={'tag': tag}) as resp:
            pprint(resp)
            if int(resp.status) == 200:
                json = await resp.json()
                values = '`\n`'.join(json[:10])
                pprint(values)
            else:
                json = await resp.json()
                pprint(json)

async def save(tag: str, text: str) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{API_URL}/push', json={'tag1': tag, 'tag2': text}) as resp:
            pprint(resp)
            if int(resp.status) == 200:
                json = await resp.json()
                pprint(json)
                values = list(json.values())[0]
                values = '`\n`'.join(values[:10])
            else:
                json = await resp.json()
                pprint(json)

asyncio.run(pull('discord.py'))
