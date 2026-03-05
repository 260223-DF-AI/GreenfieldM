# main.py
import os

from analysis import (
    load_data,
    explore_data,
    clean_data,
    add_time_features,
    sales_by_category,
    sales_by_region,
    top_products,
    daily_sales_trend,
    customer_analysis,
    weekend_vs_weekday,
)

from visualizations import (
    create_category_bar_chart,
    create_regional_pie_chart,
    create_sales_trend_line,
    create_dashboard,
)


def print_summary_report(df, category_df, region_df, top_products_df, daily_df, customer_df, weekend_weekday):
    print("\n" + "=" * 70)
    print("E-COMMERCE ORDERS ANALYTICS SUMMARY")
    print("=" * 70)

    total_orders = df["order_id"].nunique()
    total_revenue = df["total_amount"].sum()
    total_units = df["quantity"].sum()
    avg_order_value = total_revenue / total_orders if total_orders else 0

    print(f"Total Orders:        {total_orders:,}")
    print(f"Total Units Sold:    {total_units:,}")
    print(f"Total Revenue:       ${total_revenue:,.2f}")
    print(f"Avg Order Value:     ${avg_order_value:,.2f}")

    if "order_date" in df.columns:
        print(f"Date Range:          {df['order_date'].min().date()} to {df['order_date'].max().date()}")

    print("\nTop Categories by Sales:")
    for _, row in category_df.head(5).iterrows():
        print(f" - {row['category']}: ${row['total_sales']:,.2f} ({int(row['order_count']):,} orders)")

    print("\nTop Regions by Sales:")
    for _, row in region_df.head(5).iterrows():
        print(f" - {row['region']}: ${row['total_sales']:,.2f} ({row['percentage_of_total']:.1f}%)")

    print("\nTop Products by Sales:")
    for _, row in top_products_df.head(5).iterrows():
        print(f" - {row['product_name']} ({row['category']}): ${row['total_sales']:,.2f} ({int(row['units_sold']):,} units)")

    print("\nWeekend vs Weekday:")
    print(f" Weekend Sales:      ${weekend_weekday['weekend_total_sales']:,.2f} ({weekend_weekday['weekend_percentage']:.1f}%)")
    print(f" Weekday Sales:      ${weekend_weekday['weekday_total_sales']:,.2f} ({weekend_weekday['weekday_percentage']:.1f}%)")

    # Quick customer stat
    if not customer_df.empty:
        top_customer = customer_df.iloc[0]
        print("\nTop Customer by Spend:")
        print(
            f" {top_customer['customer_id']}: ${top_customer['total_spent']:,.2f} "
            f"({int(top_customer['order_count']):,} orders), Favorite: {top_customer['favorite_category']}"
        )

    # Recent daily
    if not daily_df.empty:
        latest = daily_df.iloc[-1]
        print("\nMost Recent Day Summary:")
        print(f" {latest['date']}: ${latest['total_sales']:,.2f} ({int(latest['order_count']):,} orders)")

    print("\nOutputs generated (see output/ folder).")
    print("=" * 70 + "\n")


def main():
    # ---- Config ----
    input_csv = os.path.join("GreenfieldM","week2","DataAnalysis","orders.csv")  # adjust if your path differs
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # ---- 1) Load ----
    df = load_data(input_csv)

    # Optional exploration (prints dataset info)
    explore_data(df)

    # ---- 2) Clean & Transform ----
    print("TYPE BEFORE CLEAN:", type(df))
    df = clean_data(df)
    df = add_time_features(df)

    # ---- 3) Run Analyses ----
    category_df = sales_by_category(df)
    region_df = sales_by_region(df)
    top_products_df = top_products(df, n=10)
    daily_df = daily_sales_trend(df)
    customer_df = customer_analysis(df)
    weekend_weekday = weekend_vs_weekday(df)

    # ---- 4) Generate Visualizations ----
    category_chart_path = os.path.join(output_dir, "sales_by_category.png")
    region_chart_path = os.path.join(output_dir, "sales_by_region.png")
    trend_chart_path = os.path.join(output_dir, "daily_sales_trend.png")

    create_category_bar_chart(category_df, category_chart_path)
    create_regional_pie_chart(region_df, region_chart_path)
    create_sales_trend_line(daily_df, trend_chart_path)

    dashboard_path = create_dashboard(df, output_dir)

    # ---- 5) Print Summary Report ----
    print_summary_report(
        df=df,
        category_df=category_df,
        region_df=region_df,
        top_products_df=top_products_df,
        daily_df=daily_df,
        customer_df=customer_df,
        weekend_weekday=weekend_weekday,
    )

    # Helpful prints for where files are
    print("Saved charts:")
    print(f" - {category_chart_path}")
    print(f" - {region_chart_path}")
    print(f" - {trend_chart_path}")
    print(f" - {dashboard_path}")


if __name__ == "__main__":
    main()