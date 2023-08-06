import aiohttp, json

async def pickRandomFumo():
	async with aiohttp.ClientSession() as session:
		async with session.get("https://fumos.live/api/fumo") as requestFumo:
			fumoAPIText = await requestFumo.text()
			fumoJson = json.loads(fumoAPIText)
			return fumoJson["fumo"]