import asks
import ssl
import asyncio
from bs4 import BeautifulSoup
import re
from urllib.parse import urlencode
import time
import aiofiles
import json
asks.init('asyncio')
async def getP():
    p = 'http://dao-dc-any:EcwFZQLfW1P1o9N@gw-open.ntnt.io:5959'
    proxies = {
        'http': p,
        'https': p
    }
    url = 'https://www.paypal.com/signin/'

    # 创建一个不执行证书验证的 SSL 上下文
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    session = asks.Session(connections=2, ssl_context=ssl_context)
    session.proxies = {'http': proxies, 'https': proxies}
    r = await session.get(url)
    # print(r.text)
    # 获取cookies
    cookies = r.cookies
    print(cookies)
    html = r.text
    soup = BeautifulSoup(html,'html.parser')
    form = soup.find('form')
    iputs = form.find_all('input')
    formdata = {}
    for iput in iputs:
        formdata[iput['name']] = iput['value']
    print(formdata)
    # 找到fnSessionID
    fnSessionID = re.findall(r',fnSessionId: "(.*?)",sourceId:',html)[0]
    print(fnSessionID)
    formdata['login_phone'] = '18722036517'
    formdata['isSafariAutofill'] = 'false'
    formdata['phoneCode'] = 'CN +86'
    formdata['splitLoginContext'] = 'inputPhone'
    formdata['_sessionID'] = 'null'
    formdata['ads-client-context: '] = 'signin'
    formdata['isValidCtxId'] = ''
    formdata['usePassKey'] = 'true'

    f_data = {
        "SC_VERSION": "2.0.1",
        "syncStatus": "data",
        "f": fnSessionID,
        # "f": 'fnSessionId',
        "s": "UNIFIED_LOGIN_INPUT_EMAIL",
        "chk": {
            # "ts": 1703406898049,
            # "ts":"1703406898049",
            "ts": int(time.time() * 1000),
            "eteid": [7667133238, -6001869596, 11110282995, -102422248, 5283990329, 18013206702, 17342950323, 6581359225],
            "tts": 10,
        },
        "dc": "{\"screen\":{\"colorDepth\":24,\"pixelDepth\":24,\"height\":900,\"width\":1440,\"availHeight\":814,\"availWidth\":1440},\"ua\":\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36\"}",
        "d": {
            "rDT": "31163,31247,30748:41447,41471,40988:5626,5586,5132:10770,10698,10254:10843,10660,10270:36491,36259,35864:31382,31130,30743:51898,51613,51240:31427,31115,30754:16059,15742,15378:31432,31106,30745:16067,15731,15377:10952,10595,10254:46818,46447,46115:16090,15695,15376:31469,31049,30746:41723,41282,40994:46850,46399,46114:10995,10530,10254:31489,31019,30746:18304,23"
        }
    }
    ul_fdata = urlencode(f_data)
    formdata['fn_sync_data'] = ul_fdata
    formdata_encoded = urlencode(formdata)
    headers = {
        'authority': 'www.paypal.com',
        'accept': 'application/json',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'enforce_policy=gopay; cookie_check=yes; d_id=1750eba697c04b059b7dd6a9c05e29621704437000692; LANG=zh_CN%3BCN; nsid=s%3A-ciYHYyu3vf0g7Qzu5WYEL5q3YGMWyPP.aw9wi%2Feab567cZSXyZ0Zyzbrxni%2BBnEZ5kxefrrPLtU; TLTSID=91870034733716013213082062900641; TLTDID=67324520207141131136488569585177; KHcl0EuY7AKSMgfvHl7J5E7hPtK=MMJFkT1ss5S0mhfN5kwojes5R4M_hOArT0z0eaLNZXjwNkD8arkX2xJaV8d665efWG5yAnF9EJ-t3cmT; sc_f=-k9tkvekR8_xyEBDIjpRCbp4QQa1KZ3Q2PzTQW5i_QCG2llhFunmyS-yVu-QLAD0I1pr43juuCrgJxqGFB5zl49D5qw6qoAucz1K60; cookie_prefs=T%3D1%2CP%3D1%2CF%3D1%2Ctype%3Dexplicit_banner; _gcl_au=1.1.641602674.1704437580; _ga=GA1.2.1294285457.1704437580; _gid=GA1.2.471241027.1704437580; l7_az=dcg01.phx; ts_c=vr%3Dd85ca9b218c0aa3048df43d8fcc5f95b%26vt%3Dd8bfb8a118c0a55040938a95fba49805; ddi=xd-EBJyteX02Ez0L6JkmrOewMimcWIq9IH9-Hge9JJHCZuW1BArZFo2WPm-9ABpLZ5aOlD5x_fIyV2rNhFWVqEqoXhaEh-vPQ9A5UfUOigz9dqcN; tsrce=authchallengenodeweb; x-pp-s=eyJ0IjoiMTcwNDQ0NDEzNTEzMyIsImwiOiIwIiwibSI6IjAifQ; ts=vreXpYrS%3D1799138538%26vteXpYrS%3D1704445938%26vr%3Dd85ca9b218c0aa3048df43d8fcc5f95b%26vt%3Dd8bfb8a118c0a55040938a95fba49805%26vtyp%3Dreturn; tcs=main%3Aunifiedlogin%3Asplitlogin%3A%3Aemail%7CbtnNext',
        'origin': 'https://www.paypal.com',
        'referer': 'https://www.paypal.com/signin',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"120.0.6099.129"',
        'sec-ch-ua-full-version-list': '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.129", "Google Chrome";v="120.0.6099.129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"macOS"',
        'sec-ch-ua-platform-version': '"13.6.1"',
        'sec-ch-ua-wow64': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    # 将获取到的cookies添加到headers中
    headers['cookie'] = '; '.join([item.name + '=' + item.value for item in cookies])
    r = await session.post(url, data=formdata_encoded, headers=headers)
    print(r.json())
    # 使用aiofiles
    async with aiofiles.open('test.json','w')as f:
        await f.write(r.text)
    
    
    
if __name__ == '__main__':
    asyncio.run(getP())