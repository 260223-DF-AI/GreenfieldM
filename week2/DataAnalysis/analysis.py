import pandas as pd

def load_data(filepath):
    """
    Load the orders dataset.
    - Parse dates correctly
    - Handle missing values
    - Return a clean DataFrame
    """
    #load the csv file and parse the order date as date time
    df = pd.read_csv(filepath, parse_dates = ["order_date"])
    #handle any missing values in the dataset
    #fill any missing values with 0
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)
    return df

def explore_data(df):
    """
    Print basic statistics about the dataset:
    - Shape (rows, columns)
    - Data types
    - Missing value counts
    - Basic statistics for numeric columns
    - Date range covered
    """
    print("==== DATASET OVERVIEW ====")
    print(f"Shape: {df.shape}") #shape
    print(f"Data Types:\n{df.dtypes}") #data types
    print(f"Missing Values per column:\n{df.isnull().sum()}") #missing values
    print(f"Basic Statistics:\n{df.describe()}") #basic statistics
    print(f"Date Range: {df['order_date'].min()} to {df['order_date'].max()}") #date range

def clean_data(df):
    """
    Clean the dataset:
    - Remove duplicates
    - Fill or drop missing values (document your strategy)
    - Standardize text columns (strip whitespace, consistent case)
    - Add calculated columns: 'total_amount' = quantity * unit_price
    """
    # --- Guard: ensure DataFrame ---
    if isinstance(df, pd.Series):
        # If a Series was accidentally passed, convert to 1-column DataFrame
        df = df.to_frame()

    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"clean_data expected a DataFrame, got {type(df)}")

    cleaned_df = df.copy()

    # Ensure order_date is datetime (if present)
    if "order_date" in cleaned_df.columns:
        cleaned_df["order_date"] = pd.to_datetime(cleaned_df["order_date"], errors="coerce")

    # Remove duplicate rows
    cleaned_df = cleaned_df.drop_duplicates()

    # Standardize text columns
    text_cols = ["customer_id", "product_name", "category", "region"]
    for col in text_cols:
        if col in cleaned_df.columns:
            cleaned_df[col] = cleaned_df[col].astype("string").fillna("Unknown").str.strip()

    # Consistent casing
    for col in ["product_name", "category", "region"]:
        if col in cleaned_df.columns:
            cleaned_df[col] = cleaned_df[col].replace({"": "Unknown"}).str.title()

    if "customer_id" in cleaned_df.columns:
        cleaned_df["customer_id"] = cleaned_df["customer_id"].replace({"": "Unknown"}).str.upper()

    # Numeric columns
    for col in ["quantity", "unit_price"]:
        if col in cleaned_df.columns:
            cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors="coerce").fillna(0)

    # Drop rows with invalid/missing dates (needed for time features)
    if "order_date" in cleaned_df.columns:
        cleaned_df = cleaned_df.dropna(subset=["order_date"])

    # Add total_amount
    if "quantity" in cleaned_df.columns and "unit_price" in cleaned_df.columns:
        cleaned_df["total_amount"] = cleaned_df["quantity"] * cleaned_df["unit_price"]
    else:
        cleaned_df["total_amount"] = 0

    return cleaned_df

def add_time_features(df):
    """
    Add time-based features:
    - day_of_week (0=Monday, 6=Sunday)
    - month
    - quarter
    - is_weekend (boolean)
    """
    out = df.copy()
    if "order_date" not in out.columns: #ensure its in date time
        raise KeyError("Expected column 'order_date' in data frame")
    out["order_date"] = pd.to_datetime(out["order_date"], errors = 'coerce')
    out = out.dropna(subset = ["order_date"]) #if any become nat, drop
    out["day_of_week"] = out["order_date"].dt.dayofweek #0=monday, 6=sunday
    out["month"] = out["order_date"].dt.month
    out["quarter"] = out["order_date"].dt.quarter
    out["is_weekend"] = out["day_of_week"] >= 5 #5=saturday, 6=sunday
    return out

def sales_by_category(df):
    """
    Calculate total sales and order count by category.
    Returns: DataFrame with columns [category, total_sales, order_count, avg_order_value]
    Sorted by total_sales descending.
    """
    grouped = (
        df.groupby("category", dropna=False)
        .agg(
            total_sales=("total_amount", "sum"),
            order_count=("order_id", "nunique"),
        )
        .reset_index()
    )
    grouped["avg_order_value"] = grouped.apply(
        lambda r: (r["total_sales"] / r["order_count"]) if r["order_count"] else 0,
        axis=1,
    )
    grouped = grouped[["category", "total_sales", "order_count", "avg_order_value"]]
    return grouped.sort_values("total_sales", ascending=False).reset_index(drop=True)



def sales_by_region(df):
    """
    Calculate total sales by region.
    Returns: DataFrame with columns [region, total_sales, percentage_of_total]
    """
    region_totals = (
        df.groupby("region", dropna=False)["total_amount"]
        .sum()
        .reset_index()
        .rename(columns={"total_amount": "total_sales"})
    )
    grand_total = region_totals["total_sales"].sum()
    region_totals["percentage_of_total"] = (
        (region_totals["total_sales"] / grand_total) * 100 if grand_total else 0
    )
    return region_totals.sort_values("total_sales", ascending=False).reset_index(drop=True)


def top_products(df, n=10):
    """
    Find top N products by total sales.
    Returns: DataFrame with columns [product_name, category, total_sales, units_sold]
    """
    prod = (
        df.groupby(["product_name", "category"], dropna=False)
        .agg(
            total_sales=("total_amount", "sum"),
            units_sold=("quantity", "sum"),
        )
        .reset_index()
        .sort_values("total_sales", ascending=False)
        .head(n)
        .reset_index(drop=True)
    )
    return prod[["product_name", "category", "total_sales", "units_sold"]]


def daily_sales_trend(df):
    """
    Calculate daily sales totals.
    Returns: DataFrame with columns [date, total_sales, order_count]
    """
    tmp = df.copy()
    # Ensure we group by date (not full timestamp)
    tmp["date"] = pd.to_datetime(tmp["order_date"], errors="coerce").dt.date
    tmp = tmp.dropna(subset=["date"])
    daily = (
        tmp.groupby("date")
        .agg(
            total_sales=("total_amount", "sum"),
            order_count=("order_id", "nunique"),
        )
        .reset_index()
        .sort_values("date")
        .reset_index(drop=True)
    )
    return daily[["date", "total_sales", "order_count"]]


def customer_analysis(df):
    """
    Analyze customer purchasing behavior.
    Returns: DataFrame with columns [customer_id, total_spent, order_count, 
             avg_order_value, favorite_category]
    """
    cust = (
        df.groupby("customer_id", dropna=False)
        .agg(
            total_spent=("total_amount", "sum"),
            order_count=("order_id", "nunique"),
        )
        .reset_index()
    )
    cust["avg_order_value"] = cust.apply(
        lambda r: (r["total_spent"] / r["order_count"]) if r["order_count"] else 0,
        axis=1,
    )
    # Favorite category (by total spend; tie-breaker: higher quantity; then alphabetical)
    fav = (
        df.groupby(["customer_id", "category"], dropna=False)
        .agg(
            cat_sales=("total_amount", "sum"),
            cat_units=("quantity", "sum"),
        )
        .reset_index()
        .sort_values(["customer_id", "cat_sales", "cat_units", "category"], ascending=[True, False, False, True])
    )
    fav_top = fav.drop_duplicates(subset=["customer_id"], keep="first")[
        ["customer_id", "category"]
    ].rename(columns={"category": "favorite_category"})
    result = cust.merge(fav_top, on="customer_id", how="left")
    # Column order as requested
    result = result[
        ["customer_id", "total_spent", "order_count", "avg_order_value", "favorite_category"]
    ].sort_values("total_spent", ascending=False).reset_index(drop=True)
    return result

def weekend_vs_weekday(df):
    """
    Compare weekend vs weekday sales.
    Returns: Dict with weekend and weekday total sales and percentages.
    """
    tmp = df.copy()
    # Use existing is_weekend if present; otherwise derive it from order_date
    if "is_weekend" not in tmp.columns:
        od = pd.to_datetime(tmp["order_date"], errors="coerce")
        tmp["is_weekend"] = od.dt.dayofweek >= 5
    weekend_sales = tmp.loc[tmp["is_weekend"] == True, "total_amount"].sum()
    weekday_sales = tmp.loc[tmp["is_weekend"] == False, "total_amount"].sum()
    total = weekend_sales + weekday_sales
    weekend_pct = (weekend_sales / total) * 100 if total else 0
    weekday_pct = (weekday_sales / total) * 100 if total else 0
    return {
        "weekend_total_sales": weekend_sales,
        "weekday_total_sales": weekday_sales,
        "weekend_percentage": weekend_pct,
        "weekday_percentage": weekday_pct,
    }
    