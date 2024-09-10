from pydantic import BaseModel, field_validator


class Product(BaseModel):
    """Represents a product"""

    id: int
    name: str
    price: float
    is_available: bool

    @field_validator("price")
    def price_must_be_positive(cls, v):
        """Validates if price is positive"""

        if v == None:
            return 0

        if v < 0:
            raise ValueError("price must be positive")

        return v

    def checkAvailability(self):
        """Checks if product is available"""

        return self.is_available == True
