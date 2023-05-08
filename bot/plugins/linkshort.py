from requests import get as sget
import aiohttp
from configs import Config
# async def Short(url):
#     data = {}
#     data['api'] = Config.SHORTNER_API
#     data['url'] = url
#     data['format'] = 'text'
#     link = sget(Config.SHORTNER_API_LINK, params = data).text
#     return link
async def Short(link):
    url = Config.SHORTNER_API_LINK
    params = {'api': Config.SHORTNER_API, 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True) as response:
            data = await response.json()
            return data["shortenedUrl"]
