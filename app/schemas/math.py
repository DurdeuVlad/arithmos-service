from pydantic import BaseModel, Field


class PowRequest(BaseModel):
    base: float = Field(..., description="The base value for exponentiation")
    exp: float = Field(..., description="The exponent value for exponentiation")


class PowResponse(BaseModel):
    result: float = Field(..., description="Result of base ** exp")


class FibResponse(BaseModel):
    result: int = Field(..., description="The n-th Fibonacci number")


class FactResponse(BaseModel):
    result: int = Field(..., description="The factorial of n")
