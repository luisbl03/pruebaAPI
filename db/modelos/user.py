from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: Optional[str] = None
    nombre:str
    email:str
