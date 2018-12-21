from urllib.parse import urljoin
import json
from aiohttp import ClientSession as cs

class RestController:

    def __init__(self, endpoint="https://" + "api" + "." + "spacexdata" + "." + "com" + "/v2/"):
        self.endpoint = endpoint

    async def fetchasync(self):
        resp = await self.getSpaceXJson()
        try:
            return json.loads(resp)
        except ValueError as e:
            print(e)

    async def getSpaceXJson(self, subpath="launches"):
        async with cs() as session:
            try:
                print('awaiting data')
                async with session.get(urljoin(self.endpoint, subpath)) as response:
                    if response.status != 200:
                        print('An error occured')
                        return -1
                    return await response.read()
            except Exception as e:
                print(e)
                return -1
