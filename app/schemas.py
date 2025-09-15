from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreateSchema(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr = Field(title="john@example.com")
    full_name: str | None = Field(default=None, min_length=3, max_length=100)
    password: str

    @field_validator('password')
    def password_strength(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in value):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in value):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c in "!@#$%^&*()_+-=[]{};':\",.<>?/\\|" for c in value):
            raise ValueError("Password must contain a special character")
        return value


class UserOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str | None = None

    class Config:
        from_attributes = True


class JobCreateSchema(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10, max_length=1024)


class JobOutSchema(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        from_attributes = True