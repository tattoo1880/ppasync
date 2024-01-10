# 引入fastapi 和  uvicorn
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routes import items

# 实例化一个FastAPI对象
app = FastAPI()
# 跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(items.router)



# 启动命令：uvicorn main:app --reload
