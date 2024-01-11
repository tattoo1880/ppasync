from pydantic import BaseModel

class Item(BaseModel):
    num: str
    country: str
    status: str = None  # 确保默认值与字段类型匹配
    code: str = None
    msg: str = None
