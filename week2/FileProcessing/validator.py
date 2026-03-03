import logging
from datetime import datetime
from typing import List, Dict, Any, Tuple
from exceptions import InvalidDataError, MissingFieldError

logger = logging.getLogger(__name__)
REQUIRED_FIELDS = ["date", "store_id", "product", "quantity", "price"]

def is_blank(value: Any) -> bool:
    """
    Check if a value is considered blank (None, empty string, or whitespace).
    """
    return value is None or (isinstance(value, str) and value.strip() == "")

def validate_sales_record(record, line_number):
    """
    Validate a single sales record.
    
    Required fields: date, store_id, product, quantity, price
    Validation rules:
    - date must be in YYYY-MM-DD format
    - quantity must be a positive integer
    - price must be a positive number
    
    Returns: Validated record with converted types
    Raises: InvalidDataError or MissingFieldError
    """
    #required fields present and non-empty check
    for field in REQUIRED_FIELDS:
        if field not in record or is_blank(record[field]):
            raise MissingFieldError(f"Missing required field '{field}' at line {line_number}")
        
    #check date format
    date_str = str(record["date"]).strip()
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise InvalidDataError(f"Invalid date format '{date_str}' at line {line_number}. Expected YYYY-MM-DD.")
    
    #check quantity
    qty_raw = str(record["quantity"]).strip()
    try:
        quantity = int(qty_raw)
    except ValueError:
        raise InvalidDataError(f"Quantity '{qty_raw}' is not an integer at line {line_number}.")
    if quantity <= 0:
        raise InvalidDataError(f"Quantity '{quantity}' must be a positive integer at line {line_number}.")
    
    #check pricing
    price_raw = str(record["price"]).strip()
    try:
        price = float(price_raw)
    except ValueError:
        raise InvalidDataError(f"Price '{price_raw}' is not a number at line {line_number}.")
    if price <= 0:
        raise InvalidDataError(f"Price '{price}' must be a positive number at line {line_number}.")
    
    #clean strings
    store_id = str(record["store_id"]).strip()
    product = str(record["product"]).strip()

    #return validated sales record
    return{
        "date": date_str,
        "store_id": store_id,
        "product": product,
        "quantity": quantity,
        "price": price,
    }

def validate_all_records(records):
    """
    Validate all records, collecting errors instead of stopping.
    
    Returns: Tuple of (valid_records, error_list)
    """
    valid: List[Dict[str, Any]] = []
    errors: List[str] = []

    #go through each record, starting from below the header(line 2)
    for i, record in enumerate(records,start = 2):
        try:
            valid.append(validate_sales_record(record, i))
        except (InvalidDataError, MissingFieldError) as e:
            msg = str(e)
            logger.info("Validation error at line %d: %s", i, msg)
            errors.append(msg)
    return valid, errors