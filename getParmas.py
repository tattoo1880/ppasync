import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import json
import re
import time
from getProxy import get_proxy
from functools import wraps

def timeout(limit):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # 使用 asyncio.wait_for 来设置超时
                return await asyncio.wait_for(func(*args, **kwargs), timeout=limit)
            except asyncio.TimeoutError:
                print(f"Function {func.__name__} timed out after {limit} seconds.")
                # return None  # 或者任何适当的超时响应
                return {"status": "timeout", "args": args, "kwargs": kwargs}

        return wrapper
    return decorator



@timeout(30)
async def getParams(num):
    try:
        phoneNumber = num
        url = 'https://www.paypal.com'
        url2 = 'https://www.paypal.com/signin/'
        # p = get_proxy()
        p = 'http://brd-customer-hl_e0ead291-zone-data_center:8ihxdje2oh0k@brd.superproxy.io:22225'
        if p:
            proxy = p
        else:
            return {
                "status": 3,
                "result": phoneNumber
            }
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        # async with aiohttp.ClientSession() as session:
            async with session.get(url,proxy=proxy) as resp:
                # 获取cookies
                cookies = resp.cookies
                # print(cookies)
            fnSessionId = ''
            formdata = {}
            async with session.get(url2,proxy=proxy) as resp2:
                html = await resp2.text()
                match = re.search(r"fnSessionId: '([^']+)'", html)
                if match:
                    fnSessionId = match.group(1)
                if fnSessionId:
                    print(fnSessionId)
                    soup = BeautifulSoup(html, 'html.parser')
                    # 找到有nonce属性的script标签
                    form = soup.find('form')
                    # print(form)
                    iputs = form.find_all('input')
                    formdata = {input.get('name'): input.get('value')
                                for input in iputs}
                    print(formdata)
                else:
                    return {
                            "status": 3,
                            "result": phoneNumber
                        }
            formdata['login_phone'] = phoneNumber
            formdata['isSafariAutofill'] = 'false'
            formdata['phoneCode'] = 'CN +86'
            formdata['initialSplitLoginContext'] = 'inputPhone'
            formdata['splitLoginContext'] = 'inputPhone'
            formdata['_sessionID'] = 'null'

            f_data = {
                "SC_VERSION": "2.0.1",
                "syncStatus": "data",
                "f": fnSessionId,
                # "f": 'fnSessionId',
                "s": "UNIFIED_LOGIN_INPUT_EMAIL",
                "chk": {
                    # "ts": 1703406898049,
                    # "ts":"1703406898049",
                    "ts": int(time.time() * 1000),
                    "eteid": [7667133238, -6001869596, 11110282995, -102422248, 5283990329, 18013206702, 17342950323, 6581359225],
                    "tts": 1032
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
                'Content-Type': 'application/x-www-form-urlencoded',
                'authority': 'www.paypal.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                # 'cookie': 'enforce_policy=gopay; cookie_check=yes; d_id=9bbdbf2cfb464efba58b89eaeb87a0d71703253355372; nsid=s%3A-ofVTh2lE7hQjzLNGXI2_FuJ6LmYo0Co.HDjao1oF1Y1G359YKO%2BVCi4RLzwmJFfWBZlCgciJYAE; TLTSID=23689935895036888716125580691073; TLTDID=63013829081588356910698851344931; KHcl0EuY7AKSMgfvHl7J5E7hPtK=u6ogjspxJeWFajMtGUyxftFJY9WKr-yQ9kVoAw11CjH2tkuWmGjnTFvlgUfW1BhKjxOZSY-KSTTQ6BDK; sc_f=U7zblkPGn9J6SVaahtudq-YkY2u4M80tkeho1TvyEomwnDZXutHc15WAJEsbQLJ2-7TKP9UYuihaZNsHCnTIF3Z07x2K26uO71gHnm; cookie_prefs=T%3D0%2CP%3D1%2CF%3D1%2Ctype%3Dimplicit; ddi=4ATbueLhUm1XI_xtRWt-tsLgqkTSR5q4egGUB9RTAuhvpyf-IjG2NCjLZTJERoFgc5fQJDX415AQAFyOxS-dcd0XNFo9OxSR1eXPwdL4m_T9A0i-; tsrce=unifiedloginnodeweb; x-pp-s=eyJ0IjoiMTcwMzI2MDM0ODEyNiIsImwiOiIwIiwibSI6IjAifQ; l7_az=dcg16.slc; ts_c=vr%3D91cfab4018c0a7a400c18d55fe40d2b9%26vt%3D973bbef718c0a550c86bf956fe1c64b1; ts=vreXpYrS%3D1798039033%26vteXpYrS%3D1703346433%26vr%3D91cfab4018c0a7a400c18d55fe40d2b9%26vt%3D973bbef718c0a550c86bf956fe1c64b1%26vtyp%3Dreturn',
                'pragma': 'no-cache',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-arch': '"x86"',
                'sec-ch-ua-bitness': '"64"',
                'sec-ch-ua-full-version': '"120.0.6099.71"',
                'sec-ch-ua-full-version-list': '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.71", "Google Chrome";v="120.0.6099.71"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"macOS"',
                'sec-ch-ua-platform-version': '"13.6.1"',
                'sec-ch-ua-wow64': '?0',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
            async with session.post('https://www.paypal.com/signin/', data=formdata_encoded, headers=headers,proxy=proxy) as res3:
                print(res3.status)
                # print(await res3.text())
                html = await res3.text()
                soup = BeautifulSoup(html, 'html.parser')
                p = soup.find_all(
                    'span', attrs={'class': 'profileDisplayEmail notranslate'})
                if len(p) > 0:
                    # print(p[0].text)
                    if p[0].text == phoneNumber:
                        print(phoneNumber, ' 注册')
                        return {
                            "status": 1,
                            "result": phoneNumber
                        }
                    elif p[0].text == '':
                        print(phoneNumber, '未注册')
                        return {
                            "status": 2,
                            "result": phoneNumber
                        }
                else:
                    return {
                            "status": 3,
                            "result": phoneNumber
                        }
    except:
        return {
                "status": 3,
                "result": phoneNumber
            }

async def process_batch(phoneNumbers):
    tasks = [getParams(phoneNumber) for phoneNumber in phoneNumbers]
    results = await asyncio.gather(*tasks)
    return results  # 收集这个批次的结果

async def process_all(phoneNumbers, batch_size=100):
    all_results = []  # 用于存储所有批次的结果
    for i in range(0, len(phoneNumbers), batch_size):
        batch = phoneNumbers[i:i + batch_size]
        batch_results = await process_batch(batch)
        all_results.extend(batch_results)  # 合并批次结果
    return all_results


if __name__ == '__main__':
    l = ['18612345678', '18612345679', '18612345670','18722036517']
    
    results = asyncio.run(process_all(l, 100))

    # 处理或打印结果
    for result in results:
        print(result)