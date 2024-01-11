import re
from fastapi import APIRouter,Request,BackgroundTasks
from database.crud import create_items, find_all_items, delete_all_items, find_all_items_msg,find_num
from models.model import Item
from run import start
import uuid

router = APIRouter()

tasks = {}

@router.get("/start")
async def start_job(background_tasks: BackgroundTasks):
    # 生成唯一的任务 ID
    task_id = str(uuid.uuid4())
    tasks[task_id] = "Running"
    background_tasks.add_task(long_running_task, task_id)
    return {"message": "Job started", "task_id": task_id}


async def long_running_task(task_id: str):
    try:
        print(f"Starting long-running task: {task_id}")
        res = await start()
        tasks[task_id] = "Completed"
        # print(tasks)
        # print(res)
    except Exception as e:
        tasks[task_id] = f"Failed: {e}"


@router.get("/")
async def hello():
    return {"msg": "Hello World"}



@router.get("/find")
async def find():
    # 查询所有数据
    return await find_all_items()

@router.post("/upload")
async def upload(request:Request):
    data = await request.json()
    # 遍历data.datas中的数据
    new_list = []
    for item in data['datas']:
        num = item.get('phone_number')
        country = item.get('country_code')
        # 创建Item对象
        item = Item(num=num, country=country)
        # 将Item对象插入到数据库中
        new_list.append(item.dict())
    # 批量插入数据
    print(new_list)
    res = await create_items(new_list)
    return {
        "code": 200,
        "msg": "上传成功",
        "data": 'res'
    }




@router.get("/del")
async def delete():
    # 删除所有数据
    return await delete_all_items()


@router.get("/num")
async def num():
    # 查询所有数据
    return await find_num()


@router.post("/task/status")
async def get_status(request: Request):
    data = await request.json()
    # print("=====+++====="*1000,data)
    taskId = data["task_id"]
    n = tasks[taskId]
    # print("=====+++====="*1000,n)
    return {
        'message':n
    }
@router.get("/running")
async def get_running():
    print(tasks)
    return tasks


@router.get("/delete")
async def delete():
    global tasks  # 声明要修改的全局变量
    try:
        await delete_all_items()
        tasks.clear()  # 清空全局变量 tasks
        return {"message": "删除成功"}
    except:
        return {"message": "删除失败"}
    
    
@router.get('/res')
async def find_res():
    l = await find_all_items_msg()
    # 将每个元素的 _id 从 ObjectId 转换为字符串
    print(l)  
    return {
        "message": "OK", 
        "data": l
    }
    
@router.get("/running")
async def get_running():
    print(tasks)
    return tasks
