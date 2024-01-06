from ast import main
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import json
import re
import time
from getProxy import get_proxy
from functools import wraps
import dpath
from datacode import country_code_dict
import multiprocessing
from aiohttp_retry import RetryClient, ExponentialRetry


class Work:
    def __init__(self, num,country_code):
        self.num = num
        self.country_code = country_code
    async def worker(self):
        return await getParams(self.num,self.country_code)

async def Job(num,country_code):
    work = Work(num,country_code)
    return await work.worker()



def timeout(limit):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # 使用 asyncio.wait_for 来设置超时
                return await asyncio.wait_for(func(*args, **kwargs), timeout=limit)
            except asyncio.TimeoutError:
                print(f"Function {func.__name__} timed out after {
                      limit} seconds.")
                # return None  # 或者任何适当的超时响应
                return {"status": "timeout", "args": args, "kwargs": kwargs}

        return wrapper
    return decorator


# 写一个计算时间的装饰器
def count_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} takes {end_time - start_time} seconds.")
        return res
    return wrapper

async def getParams(num,country_code):
    # print(country_code)
    country_code = "+" + f'{country_code}'
    # print(country_code)
    cc = country_code_dict.get(country_code)
    # print(cc)
    try:
            phoneNumber = num
            url = 'https://www.paypal.com'
            url2 = 'https://www.paypal.com/signin/'
            # try:
            #     p = await get_proxy()
            # except:
            #     # p = None
            p = 'http://brd-customer-hl_e0ead291-zone-data_center:8ihxdje2oh0k@brd.superproxy.io:22225'
            # p = 'http://dao-dc-any:EcwFZQLfW1P1o9N@gw-open.ntnt.io:5959'
            if p:
                proxy = p
            else:
                continue
                # return {
                #     "message": "获取代理失败",
                #     "status": 3,
                #     "result": phoneNumber
                # }
            retry_options = ExponentialRetry(attempts=10)  # 配置重试选项
            async with RetryClient(raise_for_status=False, retry_options=retry_options) as session:
            # async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.get(url2, proxy=proxy, ssl=False,timeout=5) as resp2:
                    html = await resp2.text()
                    match = re.search(r"fnSessionId: '([^']+)'", html)
                    if match:
                        try:
                            fnSessionId = match.group(1)
                        except:
                            continue
                            # return {
                            #     "message": "获取fnSessionId失败",
                            #     "status": 3,
                            #     "result": phoneNumber
                            # }
                    if fnSessionId:
                        # print(fnSessionId)
                        soup = BeautifulSoup(html, 'html.parser')
                        # 找到有nonce属性的script标签
                        form = soup.find('form')
                        # print(form)
                        iputs = form.find_all('input')
                        formdata = {input.get('name'): input.get('value')
                                    for input in iputs}
                        # print(formdata)
                    else:
                        # print("获取fnSessionId失败")
                        continue
                        # return {
                        #     "message": "获取fnSessionId失败",
                        #     "status": 3,
                        #     "result": phoneNumber
                        # }
                formdata['login_phone'] = phoneNumber
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
                async with session.post('https://www.paypal.com/signin/', data=formdata_encoded, headers=headers, proxy=proxy, ssl=False,timeout=5) as res3:
                    # print(res3.status)
                    print("正在检测手机号码是否注册", phoneNumber)
                    # print(await res3.json())
                    # print(await res3.text())
                    html = await res3.text()
                    # with open('test.json', 'w') as f:
                    #     f.write(html)
                    da = json.loads(html)
                    # print(da)
                    try:
                        result1 = dpath.get(da, '**/notifications')
                        if result1:
                            print(result1)
                            return {
                                "status": "未注册",
                                "result": phoneNumber
                            }
                    except:
                        pass
                    try:
                        result2 = dpath.get(da, '**/profile')

                        if result2:
                            print(result2)
                            return {
                                "status": "已注册",
                                "result": phoneNumber
                            }
                    except:
                        pass
    except:
        return {
            "message": "代理臭了",
            "status": "3",
            "result": num
        }

async def process_batch(phoneNumbers,country_code):
    tasks = [Job(phoneNumber,country_code) for phoneNumber in phoneNumbers]
    results = await asyncio.gather(*tasks)
    return results  # 收集这个批次的结果

async def process_all(phoneNumbers, country_code,batch_size):
    all_results = []  # 用于存储所有批次的结果
    for i in range(0, len(phoneNumbers), batch_size):
        batch = phoneNumbers[i:i + batch_size]
        batch_results = await process_batch(batch,country_code)
        all_results.extend(batch_results)  # 合并批次结果
    return all_results

# 包装一下gettParams
def wrapper(num,country_code):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        result = loop.run_until_complete(getParams(num,country_code))
        loop.close()
        return result
    except:
        loop.close()
        return {
            "message": "代理臭了",
            "status": "3",
            "result": num
        }


def process_task(num,country_code):
    result = wrapper(num,country_code)
    return result


@count_time
def main():
    # l = ['18612345678', '18612345679', '18612345670','18722036517']
    l = []
    country_code = ''
    with open('test.txt', 'r')as f:
        # 读取第一行
        line = f.readline()
        country_code = line.strip().split('-')[0]
    with open('test.txt', 'r')as f:
        for line in f.readlines():
            l.append(line.strip().split('-')[-1])
    r_list = []
    with multiprocessing.Pool(500) as pool:
        for num in l:
            r = pool.apply_async(process_task, args=(num,country_code))
            r_list.append(r)
        pool.close()
        pool.join()
        
    results = [r.get() for r in r_list]
    print(results)
    with open('result.json', 'w')as f:
        f.write(str(results))
                    
                    
                    
if __name__ == '__main__':
    main()