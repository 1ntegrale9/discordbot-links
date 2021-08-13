import aiohttp
import os


class GoogleAppScriptClient():
    def __init__(self, sheet):
        self.url = os.getenv('GAS_URL')
        self.sheet = sheet

    async def get(self) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, params={'sheet', self.sheet}) as resp:
                return await resp.json()

    async def post(self, data: dict) -> int:
        payload = {'sheet': self.sheet} | data
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=payload) as resp:
                return resp.status
