import asyncio
import aiohttp
from aiohttp import ClientConnectorError

from tracardi_plugin_sdk.domain.result import Result


class PostMan():
    def __init__(self, key):
        self.key = key

    async def send(self, string):
        try:
            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                params = {
                    'key': self.key,
                    'txt': string
                }
                async with session.request(
                        method="POST",
                        url=str("https://api.meaningcloud.com/lang-4.0/identification"),
                        data=params
                ) as response:
                    result = {
                        "status": response.status,
                        "body": await response.json()
                    }

                    if response.status in [200, 201, 202, 203, 204]:

                        return Result(port="response", value=result), Result(port="error", value=None)
                    else:
                        return Result(port="response", value=None), Result(port="error", value=result)
        except ClientConnectorError as e:
            return Result(port="response", value=None), Result(port="error", value=str(e))

        except asyncio.exceptions.TimeoutError:

            return Result(port="response", value=None), Result(port="error", value="Timeout.")
