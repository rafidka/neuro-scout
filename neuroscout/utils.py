import asyncio
from functools import wraps
from typing import Callable, Any


def max_concurrent_calls(
    limit: int,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to limit the number of concurrent asynchronous function calls.

    Args:
        limit (int): The maximum number of concurrent asynchronous function calls allowed.

    Returns:
        function: A decorator that wraps the given function to enforce the concurrency limit.

    Example:
        @max_concurrent_calls(3)
        async def my_async_function():
            # Your async code here
    """
    semaphore = asyncio.Semaphore(limit)

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Ensure that only up to 'limit' number of async tasks can run concurrently
            async with semaphore:
                return await func(*args, **kwargs)

        return wrapper

    return decorator
