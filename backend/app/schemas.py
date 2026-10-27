from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    book_title: str = Field(min_length=1)
    borrower_name: str = Field(min_length=1)
    status: str = Field(min_length=1)


class SessionOut(BaseModel):
    id: int
    book_title: str
    borrower_name: str
    status: str

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=128,
    )


class UserOut(BaseModel):
    id: int
    username: str
    role: str