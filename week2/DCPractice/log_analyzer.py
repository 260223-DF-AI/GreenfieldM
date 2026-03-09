from decorators import timer, logger, cache
from generators import read_lines, batch, filter_errors
from pipeline import create_pipeline
from collections import Counter

@timer
@logger
def analyze_logs(log_path):
    """
    Analyze a log file and return statistics.
    
    Uses generators for memory-efficient processing.
    Uses decorators for timing and logging.
    """
    level_counts = count_by_level(log_path)
    error_summary = get_error_summary(log_path, top_n=10)
    cache_stats = parse_log_line.cache_info()
    return {
        "levels": dict(level_counts),
        "top_errors": error_summary,
        "cache": {
            "hits": cache_stats.hits,
            "misses": cache_stats.misses,
            "max_size": cache_stats.max_size,
            "current_size": cache_stats.current_size,
        }
    }

@cache(max_size=1000)
def parse_log_line(line):
    """
    Parse a single log line into structured data.
    Cached because the same line format appears often.
    """
    parts = line.split(" ", 3)
    if len(parts) < 4:
        return {
            "timestamp": "",
            "level": "UNKNOWN",
            "message": line
        }
    timestamp = f"{parts[0]} {parts[1]}"
    remainder = parts[3]
    remainder_parts = remainder.split(" ", 1)
    if len(remainder_parts) == 2:
        level = remainder_parts[0]
        message = remainder_parts[1]
    else:
        level = remainder_parts[0]
        message = ""
    return {
        "timestamp": timestamp,
        "level": level,
        "message": message
    }


def count_by_level(log_path):
    """
    Count log entries by level (INFO, WARNING, ERROR).
    Use generators to process without loading entire file.
    """
    counts = Counter()
    for line in read_lines(log_path):
        parsed = parse_log_line(line)
        counts[parsed["level"]] += 1
    return counts


def get_error_summary(log_path, top_n=10):
    """
    Get top N most common error messages.
    """
    errors = Counter()
    for line in filter_errors(read_lines(log_path)):
        parsed = parse_log_line(line)
        message = parsed.get("message", "")
        errors[message] += 1
    # Ensure list of tuples (message, count)
    return list(errors.most_common(top_n))


def process_logs_in_batches(log_path, batch_size=1000):
    """
    Process logs in batches for database insertion.
    Yields batches of parsed log entries.
    """
    parsed_logs = (parse_log_line(line) for line in read_lines(log_path))
    yield from batch(parsed_logs, batch_size)

if __name__ == "__main__":
    log_file = "samples/app.log"

    print("\n=== Log Analysis ===\n")
    results = analyze_logs(log_file)
    print()

    print("Log Level Counts:")
    for level, count in results["levels"].items():
        print(f"- {level}: {count}")

    print("\nTop Error Messages:")
    for index, item in enumerate(results["top_errors"], start=1):
        message, count = item
        print(f'{index}. "{message}" ({count})')

    cache_data = results["cache"]
    total = cache_data["hits"] + cache_data["misses"]
    hit_rate = (cache_data["hits"] / total * 100) if total else 0.0

    print("\nCache Statistics:")
    print(f"- Hits: {cache_data['hits']}")
    print(f"- Misses: {cache_data['misses']}")
    print(f"- Hit Rate: {hit_rate:.1f}%")
    print()