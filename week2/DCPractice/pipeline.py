import csv
from io import StringIO

def create_pipeline(*stages):
    """
    Create a processing pipeline from multiple generator functions.
    
    Usage:
        pipeline = create_pipeline(
            read_lines,
            parse_json,
            filter_valid,
            transform
        )
        
        for result in pipeline('input.json'):
            save(result)
    """
    def pipeline(data):
        result = data
        for stage in stages:
            result = stage(result)
        return result
    return pipeline


# Example pipeline stages:

def parse_csv_line(lines):
    """Convert CSV lines to dictionaries."""
    iterator = iter(lines)
    try:
        header_line = next(iterator)
    except StopIteration:
        return
    headers = next(csv.reader([header_line]))
    for line in iterator:
        try:
            values = next(csv.reader([line]))
            if len(values) != len(headers):
                continue
            yield dict(zip(headers, values))
        except Exception:
            continue 


def validate_records(records):
    """Yield only valid records, skip invalid ones."""
    for record in records:
        if not isinstance(record, dict):
            continue
        if all(value is not None and str(value).strip() != "" for value in record.values()):
            yield record 


def enrich_records(records):
    """Add calculated fields to each record."""
    for record in records:
        enriched = dict(record)
        enriched["record_length"] = len(record)
        enriched["is_active"] = str(record.get("status", "")).lower() == "active"
        yield enriched


def deduplicate(records, key_field):
    """Yield unique records based on a key field."""
    seen = set()
    for record in records:
        if not isinstance(record, dict):
            continue
        key = record.get(key_field)
        if key not in seen:
            seen.add(key)
            yield record