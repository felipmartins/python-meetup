from pydantic import BaseModel, field_validator


class Product(BaseModel):
    id: int
    name: str
    price: float

    @field_validator("price")
    def price_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("price must be positive")
        return v
