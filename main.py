import httpx
import asyncio
from datacode import country_code_dict
from bs4 import BeautifulSoup
import re
from urllib.parse import urlencode
import time
import dpath
# 倒入进程池
from concurrent.futures import ProcessPoolExecutor
import aiofiles


async def getP(num, country_code):
    cc = country_code_dict.get("+" + country_code)
    print(cc)
    # print(country_code)
    num = str(num)
    try:
        p = 'http://dao-dc-any:EcwFZQLfW1P1o9N@gw-open.ntnt.io:5959'
        country_code = "+" + f'{country_code}'
        # print(country_code)
        # cc = country_code_dict.get(country_code)
        # print(cc)
        res = ''
        url = "https://www.paypal.com/c2/signin/"
        async with httpx.AsyncClient(timeout=10, proxies=p) as client:
            resp = await client.get(url)
            res = resp.text
            match = re.search(r"fnSessionId: '([^']+)'", res)
            if match:
                try:
                    fnSessionId = match.group(1)
                except:
                    return{
                        "num":num,
                        "code": 500,
                        "msg": "fnSessionId获取失败"
                    }
            soup = BeautifulSoup(res, "html.parser")
            forms = soup.find_all("form")
            inputs = forms[0].find_all("input")
            formdata = {}
            for i in inputs:
                if i.get("name") != None:
                    formdata[i.get("name")] = i.get("value")
            formdata['login_phone'] = num
            formdata['isSafariAutofill'] = 'false'
            formdata['phoneCode'] = cc
            formdata['splitLoginContext'] = 'inputPhone'
            formdata['_sessionID'] = 'null'
            formdata['ads-client-context: '] = 'signin'
            formdata['isValidCtxId'] = ''
            formdata['usePassKey'] = 'true'
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
                    "tts": 10,
                },
                "dc": "{\"screen\":{\"colorDepth\":24,\"pixelDepth\":24,\"height\":900,\"width\":1440,\"availHeight\":814,\"availWidth\":1440},\"ua\":\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36\"}",
                "d": {
                    "rDT": "31163,31247,30748:41447,41471,40988:5626,5586,5132:10770,10698,10254:10843,10660,10270:36491,36259,35864:31382,31130,30743:51898,51613,51240:31427,31115,30754:16059,15742,15378:31432,31106,30745:16067,15731,15377:10952,10595,10254:46818,46447,46115:16090,15695,15376:31469,31049,30746:41723,41282,40994:46850,46399,46114:10995,10530,10254:31489,31019,30746:18304,23"
                }
            }
            print(formdata)
            print(fnSessionId)
            ul_fdata = urlencode(f_data)
            formdata['fn_sync_data'] = ul_fdata
            formdata_encoded = urlencode(formdata)
            headers = {
                'authority': 'www.paypal.com',
                'accept': 'application/json',
                'accept-language': 'zh-CN,zh;q=0.9',
                'content-type': 'application/x-www-form-urlencoded',
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

            ress = await client.post(url, data=formdata_encoded, headers=headers)
            # print(ress.json())
            text_res = ress.json()
            # da = json.loads(str(text_res))
            try:
                result1 = dpath.get(text_res,"**/notifications")
                if result1:
                    print(result1,"未注册")
                    return {
                        "num":num,
                        "code": 200,
                        "msg": "未注册"
                    }
            except:
                pass
            try:
                result2 = dpath.get(text_res,"**/profile")
                if result2:
                    print(result2,"已注册")
                    await write_file('result.txt', num)
                    return {
                        "num":num,
                        "code": 200,
                        "msg": "已注册"
                    }
            except:
                pass
    except:
        return {
            "num":num,
            "code": 500,
            "msg": "请求失败"
        }
                
            
            


async def run():
    p_list = []
    country = ''
    with open('test.txt', 'r') as f:
        line = f.readline()
        country = line.strip().split('-')[0]
    with open('test.txt', 'r') as f:
        for line in f.readlines():
            num = line.strip().split('-')[1]
            p_list.append(num)
            
    print(p_list)
    print(country)
    # 使用gather函数，同时发送多个请求
    tasks = [getP(num, country) for num in p_list]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)

async def process_subset(subset, country):
    # 使用gather函数，同时发送多个请求
    tasks = [getP(num, country) for num in subset]
    results = await asyncio.gather(*tasks)
    return results
def start_asyncio_loop(subset, country):
    res = asyncio.run(process_subset(subset, country))
    return res

def split_into_chunks(lst, n):
    """将列表 lst 分割成 n 份"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
async def write_file(filename, data):
    async with aiofiles.open(filename, 'a') as file:
        await file.write(data + '\n')

        
if __name__ == '__main__':
    start = time.time()
    p_list = []
    country = ''
    with open('test.txt', 'r') as f:
        line = f.readline()
        country = line.strip().split('-')[0]
    with open('test.txt', 'r') as f:
        for line in f.readlines():
            num = line.strip().split('-')[1]
            p_list.append(num)
            
    print(p_list)
    print(country)
    subsets = list(split_into_chunks(p_list, 100))
    re_he = []
    with ProcessPoolExecutor(max_workers=20) as executor:
        results = executor.map(start_asyncio_loop, subsets, [country]*len(subsets))
        for result in results:
            # print(result)
            # 拼接所有
            re_he.extend(result)
    print(re_he)
    # 遍历re_he找到已注册的                  
    end = time.time()
    print('Cost time:', end - start)
