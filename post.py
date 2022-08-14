from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):
    title: str
    content: str
    published: bool = True # if user does not provide published then by default is True
    rating: Optional[int] = None
