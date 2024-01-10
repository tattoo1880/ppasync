from .db import collection
from models.model import Item


# 创建数据
async def create_item(item: Item):
    # 将pydantic的model转换为dict
    item_dict = item.model_dump()
    # 将dict插入到数据库中
    result = await collection.insert_one(item_dict)
    # 将插入的数据查询出来
    return await collection.find_one({"_id": result.inserted_id})

# 批量创建数据
async def create_items(items: list):
    # 将pydantic的model转换为dict
    item_list = [item.model_dump() for item in items]
    # 将dict插入到数据库中
    result = await collection.insert_many(item_list)
    # 将插入的数据查询出来
    return await find_all_items()


# 查找所有数据
async def find_all_items():
    # 将数据库中的数据查询出来
    cursor = collection.find({})
    # 将查询出来的数据转换为list
    items = [item async for item in cursor]
    
    # Optionally, you can convert ObjectId to strings as mentioned in the previous response
    return [item | {"_id": str(item["_id"])} for item in items]

# 查找所有msg为已注册的数据
async def find_all_items_msg():
    # 将数据库中的数据查询出来
    cursor = collection.find({"msg": "已注册"})
    # 将查询出来的数据转换为list
    items = [item async for item in cursor]
    return items

# 删除所有数据
async def delete_all_items():
    # 将数据库中的数据删除
    res = await collection.delete_many({})
    if res.deleted_count:
        return {"msg": "删除成功"}
    else:
        return {"msg": "删除失败"}

# 找到所有status，code, msg == None
async def find_all_status():
    # 将数据库中的数据查询出来
    cursor = collection.find({"status": None, "code": None, "msg": None})
    # 将查询出来的数据转换为list
    return cursor

async def find_num():
    custor = await find_all_items()
    num = len(custor)
    return {
        "code": 200,
        "msg": "查询成功",
        "长度": num
    }
    
# update
async def update_item(item: Item):
    # 将pydantic的model转换为dict
    item_dict = item
    # 将dict插入到数据库中
    result = await collection.update_one({"num": item_dict['num']}, {"$set": item_dict})
    # 将插入的数据查询出来
    return await collection.find_one({"num": item_dict['num']})

# 根据列表批量更新
async def update_items(list: list):
    # 将pydantic的model转换为dict
    item_list = list
    # print(item_list)
    # 将dict插入到数据库中
    for item in item_list:
        await collection.update_one({"num": item['num']}, {"$set": item})
    # 将插入的数据查询出来
    return await find_all_items()