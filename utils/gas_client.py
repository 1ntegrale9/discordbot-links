import aiohttp

async def get(url, sheet_name) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params={'sheet', sheet_name}) as resp:
            return await resp.json()

async def post(url, sheet_name, data: dict) -> int:
    payload = {'sheet': sheet_name} | data
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            return resp.status
