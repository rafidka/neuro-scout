import pytest
import asyncio
from neuroscout.utils import max_concurrent_calls


@pytest.mark.asyncio
async def test_max_concurrent_calls():
    results: list[int] = []

    @max_concurrent_calls(2)
    async def limited_function(index: int):
        await asyncio.sleep(0.1)
        results.append(index)

    async def run_tasks():
        tasks = [limited_function(i) for i in range(5)]
        await asyncio.gather(*tasks)

    await run_tasks()

    # Check that all tasks have been executed
    assert len(results) == 5


@pytest.mark.asyncio
async def test_max_concurrent_calls_limit():
    call_count = 0
    max_call_count = 0

    @max_concurrent_calls(2)
    async def limited_function():
        nonlocal call_count, max_call_count

        call_count += 1
        max_call_count = max(max_call_count, call_count)
        await asyncio.sleep(1)
        call_count -= 1

    tasks = [limited_function() for _ in range(10)]
    await asyncio.gather(*tasks)

    assert max_call_count == 2
