import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd

def create_category_bar_chart(category_data, output_path):
    """
    Create a horizontal bar chart of sales by category.
    - Include value labels on bars
    - Use a professional color scheme
    - Save to output_path
    """
    # Accept either DataFrame with columns or Series-like input
    if isinstance(category_data, pd.DataFrame):
        if "category" not in category_data.columns or "total_sales" not in category_data.columns:
            raise KeyError("category_data must have columns ['category', 'total_sales'].")
        plot_df = category_data[["category", "total_sales"]].copy()
    else:
        raise TypeError("category_data must be a pandas DataFrame with ['category','total_sales'].")
    # Sort so largest appears at top in horizontal bar chart
    plot_df = plot_df.sort_values("total_sales", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(plot_df["category"], plot_df["total_sales"])
    ax.set_title("Total Sales by Category")
    ax.set_xlabel("Total Sales")
    ax.set_ylabel("Category")
    # Value labels
    max_val = plot_df["total_sales"].max() if len(plot_df) else 0
    pad = max_val * 0.01 if max_val else 0.5
    for bar in bars:
        width = bar.get_width()
        ax.text(width + pad, bar.get_y() + bar.get_height() / 2, f"{width:,.2f}", va="center")
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    plt.savefig(output_path, dpi=200)
    plt.close(fig)

def create_regional_pie_chart(region_data, output_path):
    """
    Create a pie chart showing sales distribution by region.
    - Include percentages
    - Use distinct colors for each region
    - Save to output_path
    """
    if not isinstance(region_data, pd.DataFrame):
        raise TypeError("region_data must be a pandas DataFrame with ['region','total_sales'].")
    if "region" not in region_data.columns or "total_sales" not in region_data.columns:
        raise KeyError("region_data must have columns ['region', 'total_sales'].")
    plot_df = region_data[["region", "total_sales"]].copy()
    plot_df = plot_df.sort_values("total_sales", ascending=False)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        plot_df["total_sales"],
        labels=plot_df["region"],
        autopct="%1.1f%%",
        startangle=90,
    )
    ax.set_title("Sales Distribution by Region")
    ax.axis("equal")
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    plt.savefig(output_path, dpi=200)
    plt.close(fig)

def create_sales_trend_line(daily_data, output_path):
    """
    Create a line chart showing daily sales trend.
    - Include moving average (7-day)
    - Mark weekends differently
    - Add proper axis labels and title
    - Save to output_path
    """
    if not isinstance(daily_data, pd.DataFrame):
        raise TypeError("daily_data must be a pandas DataFrame with ['date','total_sales'].")
    if "date" not in daily_data.columns or "total_sales" not in daily_data.columns:
        raise KeyError("daily_data must have columns ['date', 'total_sales'] (and optionally order_count).")
    plot_df = daily_data.copy()
    plot_df["date"] = pd.to_datetime(plot_df["date"], errors="coerce")
    plot_df = plot_df.dropna(subset=["date"]).sort_values("date")
    plot_df["ma_7"] = plot_df["total_sales"].rolling(window=7, min_periods=1).mean()
    plot_df["is_weekend"] = plot_df["date"].dt.dayofweek >= 5
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(plot_df["date"], plot_df["total_sales"], label="Daily Sales")
    ax.plot(plot_df["date"], plot_df["ma_7"], label="7-Day Moving Avg")
    # Mark weekends differently (scatter weekend points)
    weekend_df = plot_df[plot_df["is_weekend"]]
    if not weekend_df.empty:
        ax.scatter(weekend_df["date"], weekend_df["total_sales"], label="Weekend")
    ax.set_title("Daily Sales Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Sales")
    ax.legend()
    fig.autofmt_xdate()
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    plt.savefig(output_path, dpi=200)
    plt.close(fig)

def create_dashboard(df, output_dir):
    """
    Create a multi-panel dashboard with 4 subplots:
    1. Sales by category (bar)
    2. Sales by region (pie)
    3. Daily trend (line)
    4. Top 10 products (horizontal bar)
    
    Save as a single figure.
    """
    os.makedirs(output_dir, exist_ok=True)
    # Build needed aggregations from raw df (expects cleaned df with total_amount + order_date)
    required_cols = {"category", "region", "product_name", "quantity", "total_amount", "order_id", "order_date"}
    missing = required_cols - set(df.columns)
    if missing:
        raise KeyError(f"Dashboard requires columns: {sorted(required_cols)}. Missing: {sorted(missing)}")
    # Category
    category_data = (
        df.groupby("category")
        .agg(total_sales=("total_amount", "sum"))
        .reset_index()
        .sort_values("total_sales", ascending=False)
    )
    # Region
    region_data = (
        df.groupby("region")
        .agg(total_sales=("total_amount", "sum"))
        .reset_index()
        .sort_values("total_sales", ascending=False)
    )
    # Daily
    tmp = df.copy()
    tmp["date"] = pd.to_datetime(tmp["order_date"], errors="coerce").dt.date
    tmp = tmp.dropna(subset=["date"])
    daily_data = (
        tmp.groupby("date")
        .agg(
            total_sales=("total_amount", "sum"),
            order_count=("order_id", "nunique"),
        )
        .reset_index()
        .sort_values("date")
    )
    daily_data["date"] = pd.to_datetime(daily_data["date"])
    daily_data["ma_7"] = daily_data["total_sales"].rolling(window=7, min_periods=1).mean()
    daily_data["is_weekend"] = daily_data["date"].dt.dayofweek >= 5
    # Top products
    top_products = (
        df.groupby(["product_name", "category"])
        .agg(
            total_sales=("total_amount", "sum"),
            units_sold=("quantity", "sum"),
        )
        .reset_index()
        .sort_values("total_sales", ascending=False)
        .head(10)
    )
    top_products = top_products.sort_values("total_sales", ascending=True)  # for barh
    # Create dashboard figure
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    ax1, ax2, ax3, ax4 = axes[0, 0], axes[0, 1], axes[1, 0], axes[1, 1]

    # 1) Sales by category (barh)
    cat_sorted = category_data.sort_values("total_sales", ascending=True)
    bars1 = ax1.barh(cat_sorted["category"], cat_sorted["total_sales"])
    ax1.set_title("Sales by Category")
    ax1.set_xlabel("Total Sales")
    max_val = cat_sorted["total_sales"].max() if len(cat_sorted) else 0
    pad = max_val * 0.01 if max_val else 0.5
    for b in bars1:
        w = b.get_width()
        ax1.text(w + pad, b.get_y() + b.get_height() / 2, f"{w:,.0f}", va="center")

    # 2) Sales by region (pie)
    ax2.pie(
        region_data["total_sales"],
        labels=region_data["region"],
        autopct="%1.1f%%",
        startangle=90,
    )
    ax2.set_title("Sales by Region")
    ax2.axis("equal")

    # 3) Daily trend (line + MA + weekend markers)
    ax3.plot(daily_data["date"], daily_data["total_sales"], label="Daily Sales")
    ax3.plot(daily_data["date"], daily_data["ma_7"], label="7-Day Moving Avg")
    wk = daily_data[daily_data["is_weekend"]]
    if not wk.empty:
        ax3.scatter(wk["date"], wk["total_sales"], label="Weekend")
    ax3.set_title("Daily Sales Trend")
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Total Sales")
    ax3.legend()
    fig.autofmt_xdate()

    # 4) Top 10 products (barh)
    # Use product_name labels; include category in label to reduce ambiguity
    top_labels = top_products.apply(lambda r: f"{r['product_name']} ({r['category']})", axis=1)
    bars4 = ax4.barh(top_labels, top_products["total_sales"])
    ax4.set_title("Top 10 Products by Sales")
    ax4.set_xlabel("Total Sales")
    max_val4 = top_products["total_sales"].max() if len(top_products) else 0
    pad4 = max_val4 * 0.01 if max_val4 else 0.5
    for b in bars4:
        w = b.get_width()
        ax4.text(w + pad4, b.get_y() + b.get_height() / 2, f"{w:,.0f}", va="center")
    plt.tight_layout()
    output_path = os.path.join(output_dir, "dashboard.png")
    plt.savefig(output_path, dpi=200)
    plt.close(fig)
    return output_path