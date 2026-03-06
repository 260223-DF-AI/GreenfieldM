import pytest
import asyncio
from decorators import timer, retry, cache, async_retry, rate_limit, validate_args

def test_timer_returns_result():
    """Timer decorator should not affect return value."""
    @timer
    def multiply(a,b):
        return a * b
    assert multiply(3, 4) == 12

def test_retry_succeeds_eventually():
    """Retry should succeed if function works within attempts."""
    attempts = {"count": 0}

    @retry(max_attempts=3, delay=0, exceptions = (ValueError,))
    def flaky():
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise ValueError("temporary failure")
        return "Success"

    assert flaky() == "Success"
    assert attempts["count"] == 3

def test_cache_returns_cached_value():
    """Cache should return same value without recomputing."""
    calls = {"count": 0}

    @cache(max_size = 10)
    def square(x):
        calls["count"] += 1
        return x * x
    
    assert square(5) == 25
    assert square(5) == 25
    assert calls["count"] == 1

def test_cache_info_tracks_hits():
    """Cache info should track hits and misses."""
    @cache(max_size=10)
    def add_one(x):
        return x + 1

    add_one.cache_clear()
    add_one(1)
    add_one(1)
    add_one(2)

    info = add_one.cache_info()
    assert info.hits == 1
    assert info.misses == 2

def test_retry_raises_after_max_attempts():
    """Retry should raise after all attempts fail."""
    @retry(max_attempts=2, delay=0, exceptions=(ValueError,))
    def always_fail():
        raise ValueError("Nope")

    with pytest.raises(ValueError):
        always_fail()

def test_rate_limit_allows_calls_within_limit():
    @rate_limit(max_calls=2, period=60)
    def hello():
        return "hi"

    assert hello() == "hi"
    assert hello() == "hi"


def test_rate_limit_blocks_extra_calls():
    @rate_limit(max_calls=2, period=60)
    def hello():
        return "hi"

    hello()
    hello()

    with pytest.raises(RuntimeError):
        hello()


def test_validate_args_accepts_correct_types():
    @validate_args
    def add(a: int, b: int) -> int:
        return a + b

    assert add(2, 3) == 5


def test_validate_args_rejects_wrong_types():
    @validate_args
    def add(a: int, b: int) -> int:
        return a + b

    with pytest.raises(TypeError):
        add("2", 3)


def test_async_retry_succeeds_eventually():
    attempts = {"count": 0}

    @async_retry(max_attempts=3, delay=0, exceptions=(ValueError,))
    async def flaky():
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise ValueError("fail")
        return "ok"

    result = asyncio.run(flaky())
    assert result == "ok"