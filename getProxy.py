import requests


def get_proxy():
    url = 'https://dps.kdlapi.com/api/getdps/?secret_id=olo53thb5pxv7aszrpk3&num=1&signature=gys1fa2c5wc6ud9zapyqtyntkm8vkudw&pt=1&format=json&sep=1'
    r = requests.get(url)
    # print(r.json())
    try:
        proxy = r.json()['data']['proxy_list'][0]
        return 'http://' + proxy
    except:
        return None
    
    
if __name__ == '__main__':
    get_proxy()