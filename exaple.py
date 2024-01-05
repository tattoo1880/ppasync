import asyncio

async def getParams(num):
    # 您的函数实现
    pass

async def process_batch(phoneNumbers, timeout):
    tasks = [getParams(phoneNumber) for phoneNumber in phoneNumbers]
    done, pending = await asyncio.wait(tasks, timeout=timeout)

    # 取消所有挂起（未完成）的任务
    for task in pending:
        task.cancel()

    # 收集完成的任务结果
    results = [task.result() for task in done if task.done() and not task.cancelled()]
    return results

async def process_all(phoneNumbers, batch_size=100, timeout=10):
    all_results = []
    for i in range(0, len(phoneNumbers), batch_size):
        batch = phoneNumbers[i:i + batch_size]
        batch_results = await process_batch(batch, timeout)
        all_results.extend(batch_results)
    return all_results

if __name__ == '__main__':
    phoneNumbers = ['18722036517', '18722036518', ...]  # 您的电话号码列表
    results = asyncio.run(process_all(phoneNumbers, batch_size=100, timeout=5))  # 5秒超时

    for result in results:
        print(result)
