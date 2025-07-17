"""
Core mathematical operations:
- power(base, exp): base raised to the power exp
- fibonacci(n): nth Fibonacci number
- factorial(n): factorial of n
"""

def power(base: float, exp: float) -> float:
    """
    Calculate base ** exp.
    """
    return base ** exp


def fibonacci(n: int) -> int:
    """
    Compute the nth Fibonacci number using an iterative approach.
    """
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def factorial(n: int) -> int:
    """
    Compute the factorial of n (n!).
    """
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
