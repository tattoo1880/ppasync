import httpx
import asyncio

async def get_proxy():
    url = 'https://dps.kdlapi.com/api/getdps/?secret_id=olo53thb5pxv7aszrpk3&num=1&signature=gys1fa2c5wc6ud9zapyqtyntkm8vkudw&pt=1&format=json&sep=1'
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        if resp.status_code == 200:
            return 'http://' + resp.json()['data']['proxy_list'][0]
        else:
            return None
    
    
if __name__ == '__main__':
    res = asyncio.run(get_proxy())
    print(res)