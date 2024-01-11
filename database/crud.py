from fastapi.encoders import jsonable_encoder
from .db import create_redis_pool
import json

# 批量创建数据
# 批量创建数据
async def create_items(items: list):
    ttl = 3600
    client = await create_redis_pool()
    for i in items:
        k = json.dumps(i)
        await client.set(i['num'], k)
        await client.expire(i['num'], ttl)
    return await find_all_items()
        


async def find_all_items():
    # 将数据库中的数据查询出来
    items= []
    client = await create_redis_pool()
    keys = await client.keys('*')
    for key in keys:
        value = await client.get(key)
        value = value.decode('utf-8')
        re = json.loads(value)
        items.append(re)
    return items

# 查找所有msg为已注册的数据
async def find_all_items_msg():
    # 将数据库中的数据查询出来
    items = await find_all_items()
    new_items = []
    for item in items:
        if item['msg'] == '已注册':
            new_items.append(item)
    return new_items
    
    

# 删除所有数据
async def delete_all_items():
    # 将数据库中的数据查询出来
    client = await create_redis_pool()
    keys = await client.keys('*')
    for key in keys:
        await client.delete(key)
    return await find_all_items()

# 找到所有status，code, msg == None
async def find_all_status():
    # 将数据库中的数据查询出来
    items = await find_all_items()
    new_items = []
    for item in items:
        if item['status'] == None and item['code'] == None and item['msg'] == None:
            new_items.append(item)
    return new_items


# update_items
async def update_items(items: list):
    client = await create_redis_pool()
    for i in items:
        k = json.dumps(i)
        await client.set(i['num'], k)
    return await find_all_items()


async def find_num():
    # 将数据库中的数据查询出来
    pool = await create_redis_pool()
    cursor = await pool.keys('*')
    # 将查询出来的数据转换为list
    return len(cursor)