import pytest
import pandas as pd
from analysis import *

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame({
        'order_id': [1, 2, 3],
        'customer_id': ['C001', 'C002', 'C001'],
        'order_date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-02']),
        'product_name': ['Widget', 'Gadget', 'Widget'],
        'category': ['Electronics', 'Electronics', 'Electronics'],
        'quantity': [2, 1, 3],
        'unit_price': [10.00, 25.00, 10.00],
        'region': ['North', 'South', 'North']
    })

def test_clean_data_removes_duplicates(sample_data):
    """Test that clean_data removes duplicate rows."""
    df_dup = pd.concat([sample_data, sample_data.iloc[[0]]], ignore_index=True)
    cleaned = clean_data(df_dup)
    assert len(cleaned) == len(sample_data)  # duplicate row removed


def test_clean_data_adds_total_amount(sample_data):
    """Test that clean_data creates total_amount correctly."""
    cleaned = clean_data(sample_data)
    assert "total_amount" in cleaned.columns
    # order 1: 2 * 10 = 20
    assert cleaned.loc[cleaned["order_id"] == 1, "total_amount"].iloc[0] == 20.0
    # order 2: 1 * 25 = 25
    assert cleaned.loc[cleaned["order_id"] == 2, "total_amount"].iloc[0] == 25.0


def test_clean_data_standardizes_text(sample_data):
    """Test that clean_data trims whitespace / normalizes case."""
    messy = sample_data.copy()
    messy.loc[0, "region"] = "  north  "
    messy.loc[0, "category"] = "  electronics "
    messy.loc[0, "customer_id"] = " c001 "
    cleaned = clean_data(messy)

    # Based on our clean_data implementation:
    assert cleaned.loc[cleaned["order_id"] == 1, "region"].iloc[0] == "North"
    assert cleaned.loc[cleaned["order_id"] == 1, "category"].iloc[0] == "Electronics"
    assert cleaned.loc[cleaned["order_id"] == 1, "customer_id"].iloc[0] == "C001"


def test_add_time_features_creates_columns(sample_data):
    """Test that add_time_features adds expected time columns."""
    cleaned = clean_data(sample_data)
    with_time = add_time_features(cleaned)
    for col in ["day_of_week", "month", "quarter", "is_weekend"]:
        assert col in with_time.columns


def test_sales_by_category_calculation(sample_data):
    """Test that category totals are calculated correctly."""
    df = add_time_features(clean_data(sample_data))
    cat = sales_by_category(df)

    # Only one category in sample_data
    assert len(cat) == 1
    assert cat.loc[0, "category"] == "Electronics"

    # Total sales = (2*10) + (1*25) + (3*10) = 20 + 25 + 30 = 75
    assert cat.loc[0, "total_sales"] == 75.0

    # Unique orders = 3
    assert cat.loc[0, "order_count"] == 3

    # Avg order value = 75 / 3 = 25
    assert cat.loc[0, "avg_order_value"] == 25.0


def test_sales_by_region_percentages_sum_to_100(sample_data):
    """Test that region percentages sum to ~100%."""
    df = add_time_features(clean_data(sample_data))
    reg = sales_by_region(df)

    pct_sum = reg["percentage_of_total"].sum()
    assert pct_sum == pytest.approx(100.0, abs=1e-6)


def test_top_products_returns_correct_count(sample_data):
    """Test that top_products returns requested number of items."""
    df = add_time_features(clean_data(sample_data))
    # We have 2 unique products; request 1 to ensure it respects n
    top1 = top_products(df, n=1)
    assert len(top1) == 1


def test_top_products_correct_top_item(sample_data):
    """Test that top_products picks the highest revenue product."""
    df = add_time_features(clean_data(sample_data))
    top = top_products(df, n=2)

    # Widget sales = 20 + 30 = 50
    # Gadget sales = 25
    assert top.iloc[0]["product_name"] == "Widget"
    assert top.iloc[0]["total_sales"] == 50.0


def test_daily_sales_trend_has_expected_rows(sample_data):
    """Test daily trend groups by date correctly."""
    df = add_time_features(clean_data(sample_data))
    daily = daily_sales_trend(df)

    # Dates are 2024-01-01 and 2024-01-02 => 2 rows
    assert len(daily) == 2

    # 2024-01-01 total sales = 20
    d1 = daily[daily["date"] == pd.to_datetime("2024-01-01").date()]
    assert d1["total_sales"].iloc[0] == 20.0
    assert d1["order_count"].iloc[0] == 1

    # 2024-01-02 total sales = 25 + 30 = 55
    d2 = daily[daily["date"] == pd.to_datetime("2024-01-02").date()]
    assert d2["total_sales"].iloc[0] == 55.0
    assert d2["order_count"].iloc[0] == 2


def test_customer_analysis_favorite_category(sample_data):
    """Test customer favorite category is computed and matches expected."""
    df = add_time_features(clean_data(sample_data))
    cust = customer_analysis(df)

    # Both customers only buy Electronics in sample data
    c1 = cust[cust["customer_id"] == "C001"].iloc[0]
    c2 = cust[cust["customer_id"] == "C002"].iloc[0]
    assert c1["favorite_category"] == "Electronics"
    assert c2["favorite_category"] == "Electronics"

    # C001 spent 20 + 30 = 50, order_count = 2, avg_order_value = 25
    assert c1["total_spent"] == 50.0
    assert c1["order_count"] == 2
    assert c1["avg_order_value"] == 25.0


def test_weekend_vs_weekday_returns_expected_keys(sample_data):
    """Test weekend_vs_weekday returns required fields."""
    df = add_time_features(clean_data(sample_data))
    result = weekend_vs_weekday(df)

    for key in [
        "weekend_total_sales",
        "weekday_total_sales",
        "weekend_percentage",
        "weekday_percentage",
    ]:
        assert key in result


def test_weekend_vs_weekday_percentages_sum_to_100(sample_data):
    """Test weekend/weekday percentages sum to ~100%."""
    df = add_time_features(clean_data(sample_data))
    result = weekend_vs_weekday(df)

    total_pct = result["weekend_percentage"] + result["weekday_percentage"]
    assert total_pct == pytest.approx(100.0, abs=1e-6)