"""
Concurrency helper utilities for asyncio scripts.
"""

import asyncio
from collections.abc import Awaitable, Callable, Iterable
from typing import Any, TypeVar

T = TypeVar("T")


def _ensure_coroutine(fn: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    if asyncio.iscoroutinefunction(fn):
        return fn

    async def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return wrapper


async def gather_with_concurrency(limit: int, coros: Iterable[Awaitable[T]]) -> list[T]:
    """Gather awaitables with a concurrency limit."""
    semaphore = asyncio.Semaphore(limit)

    async def run(coro: Awaitable[T]) -> T:
        async with semaphore:
            return await coro

    return await asyncio.gather(*(run(c) for c in coros))


async def run_in_batches(
    limit: int, tasks: Iterable[Callable[[], Awaitable[T]]]
) -> list[T]:
    """Run callables (returning awaitables) in batches of size `limit`."""
    results: list[T] = []
    batch: list[Callable[[], Awaitable[T]]] = []

    for task_fn in tasks:
        batch.append(task_fn)
        if len(batch) == limit:
            batch_results = await asyncio.gather(*(fn() for fn in batch))
            results.extend(batch_results)
            batch = []

    if batch:
        batch_results = await asyncio.gather(*(fn() for fn in batch))
        results.extend(batch_results)

    return results


async def cancel_on_timeout(coro: Awaitable[T], timeout: float) -> T | None:
    """Run coroutine with timeout; cancel if exceeded."""
    task = asyncio.create_task(coro)
    try:
        return await asyncio.wait_for(task, timeout=timeout)
    except asyncio.TimeoutError:
        task.cancel()
        return None
