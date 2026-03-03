
from typing import List, Dict, Any


def calculate_totals(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Calculate line totals (quantity * price) for each record.
    Returns: Records with added 'total' field
    """
    out: List[Dict[str, Any]] = []
    for r in records:
        new_r = dict(r)
        new_r["total"] = new_r["quantity"] * new_r["price"]
        out.append(new_r)
    return out

def aggregate_by_store(records: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Aggregate sales by store_id.
    Returns: Dict mapping store_id to total sales
    """
    totals: Dict[str, float] = {}
    for r in records:
        store_id = r["store_id"]
        total = r["total"]
        totals[store_id] = totals.get(store_id, 0) + total
    return totals

def aggregate_by_product(records: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Aggregate sales by product.
    Returns: Dict mapping product to total quantity sold
    """
    totals: Dict[str, int] = {}
    for r in records:
        product = r["product"]
        quantity = r["quantity"]
        totals[product] = totals.get(product, 0) + quantity
    return totals