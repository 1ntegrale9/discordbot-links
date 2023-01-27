import aiohttp
import os


class GoogleAppScriptClient():
    def __init__(self):
        self.url = os.getenv('GAS_URL')

    async def get(self, sheet_name) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, params={'sheet', sheet_name}) as resp:
                return await resp.json()

    async def post(self, sheet_name, data: dict) -> int:
        payload = {'sheet': sheet_name} | data
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=payload) as resp:
                return resp.status
