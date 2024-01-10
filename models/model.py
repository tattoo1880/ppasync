from pydantic import BaseModel
from bson import ObjectId

class Item(BaseModel):
    num: str
    country: str
    status: str = None  # 确保默认值与字段类型匹配
    code: str = None
    msg: str = None

    class Config:
        json_encoders = {
            ObjectId: lambda oid: str(oid)  # 直接将 ObjectId 转换为字符串
        }