from functools import wraps
import time
from collections import OrderedDict, namedtuple

def timer(func):
    """
    Measure and print function execution time.
    
    Usage:
        @timer
        def slow_function():
            time.sleep(1)
    
    Output: "slow_function took 1.0023 seconds"
    """
    @wraps(func)
    def wrapper(*args, **kwards):
        start = time.perf_counter()
        result = func(*args, **kwards)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

def logger(func):
    """
    Log function calls with arguments and return value.
    
    Usage:
        @logger
        def add(a, b):
            return a + b
        
        add(2, 3)
    
    Output:
        "Calling add(2, 3)"
        "add returned 5"
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        parts = [repr(arg) for arg in args]
        parts.extend(f"{key}={value!r}" for key, value in kwargs.items())
        arg_str = ", ".join(parts)

        print(f"calling{func.__name__}({arg_str})")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result!r}")
        return result
    return wrapper

def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    """
    Retry a function on failure.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Seconds to wait between retries
        exceptions: Tuple of exceptions to catch
    
    Usage:
        @retry(max_attempts=3, delay=0.5)
        def flaky_api_call():
            # might fail sometimes
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_error = exc 
                    if attempt == max_attempts:
                        raise
                    time.sleep(delay)
            raise last_error
        return wrapper
    return decorator

def cache(max_size=128):
    """
    Cache function results.
    Similar to lru_cache but with visible cache inspection.
    
    Usage:
        @cache(max_size=100)
        def expensive_computation(x):
            return x ** 2
        
        expensive_computation(5)  # Computes
        expensive_computation(5)  # Returns cached
        
        # Inspect cache
        expensive_computation.cache_info()
        expensive_computation.cache_clear()
    """
    CacheInfo = namedtuple("CacheInfo", ["hits", "misses", "max_size", "current_size"])

    def decorator(func):
        store = OrderedDict()
        hits = 0
        misses = 0

        def make_key(args, kwargs):
            return(args, tuple(sorted(kwargs.items())))
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal hits, misses
            key = make_key(args, kwargs)
            if key in store:
                hits += 1
                store.move_to_end(key)
                return store[key]
            misses += 1
            result = func(*args, **kwargs)
            store[key] = result
            store.move_to_end(key)
            if len(store) > max_size:
                store.popitem(last=False)
            return result
        
        def cache_info():
            return CacheInfo(
                hits = hits,
                misses = misses,
                max_size = max_size,
                current_size = len(store)
            )
        
        def cache_clear():
            nonlocal hits, misses
            store.clear()
            hits = 0
            misses = 0

        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        wrapper._cache = store
        return wrapper
    return decorator
        