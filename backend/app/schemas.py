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