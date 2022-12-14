from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint
################################
# Users
################################
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class  Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str

################################
# Posts
################################

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase): 
    pass

class PostOut(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True
        
class PostOutVote(BaseModel):
    Post: PostOut
    votes: int
    
    class  Config:
        orm_mode = True
    
################################
# Authorization
################################
class Token(BaseModel):
    access_token: str
    token_type: str
 
class TokenData(BaseModel):
    id: Optional[str] = None
    
################################
# Votes
################################
class VoteBase(BaseModel):
    post_id: int
    direction: conint(le=1) # 0 or 1 