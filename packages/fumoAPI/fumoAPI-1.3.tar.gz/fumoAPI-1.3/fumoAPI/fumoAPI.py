import aiohttp, json, requests

url = 'https://fumos.live/api/fumo'

async def pickRandomFumo():
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as requestFumo:
			fumoAPIText = await requestFumo.text()
			fumoJson = json.loads(fumoAPIText)
			return fumoJson["fumo"]

def randomFumo():
	requestFumo = requests.get(url).text
	fumoJson = json.loads(requestFumo)
	return fumoJson["fumo"] 