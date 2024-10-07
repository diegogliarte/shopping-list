from pydantic import BaseModel


class ShoppingItemCreate(BaseModel):
    name: str


class ShoppingItemResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
