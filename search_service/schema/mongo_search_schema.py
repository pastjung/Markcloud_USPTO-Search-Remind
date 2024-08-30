from pydantic import BaseModel

class Uspto(BaseModel):
    workmark : str
    status : str
    goods_and_service : str
    class_num : str
    serial : str
    owners : str