from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str | None = None
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    full_name: str | None = None

    class Config:
        from_attributes = True


class JobCreate(BaseModel):
    title: str
    description: str


class JobOut(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        from_attributes = True