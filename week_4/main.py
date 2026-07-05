from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "sales_data.csv"
VISUALIZATION_DIR = BASE_DIR / "visualizations"
REPORT_DIR = BASE_DIR / "report"
REPORT_PATH = REPORT_DIR / "sales_analysis_report.md"


def load_and_validate_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"The file {path} was not found.")

    try:
        df = pd.read_csv(path)
    except Exception as exc:
        raise ValueError(f"Could not read the CSV file: {exc}") from exc

    required_columns = [
        "Date",
        "Product",
        "Quantity",
        "Price",
        "Customer_ID",
        "Region",
        "Total_Sales",
    ]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df["Total_Sales"] = pd.to_numeric(df["Total_Sales"], errors="coerce")

    df = df.dropna(subset=["Date", "Quantity", "Price", "Total_Sales", "Product", "Region", "Customer_ID"])

    if df.empty:
        raise ValueError("No valid rows remained after cleaning the data.")

    df = df.sort_values("Date").reset_index(drop=True)
    return df


def analyze_sales(df: pd.DataFrame) -> dict:
    total_revenue = df["Total_Sales"].sum()
    total_units = df["Quantity"].sum()
    average_sale_value = df["Total_Sales"].mean()

    product_sales = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)
    region_sales = df.groupby("Region")["Total_Sales"].sum().sort_values(ascending=False)
    monthly_sales = (
        df.set_index("Date")
        .resample("M")["Total_Sales"]
        .sum()
        .sort_index()
    )

    return {
        "rows": len(df),
        "total_revenue": round(total_revenue, 2),
        "total_units": int(total_units),
        "average_sale_value": round(average_sale_value, 2),
        "top_product": product_sales.index[0],
        "top_product_sales": round(product_sales.iloc[0], 2),
        "top_region": region_sales.index[0],
        "top_region_sales": round(region_sales.iloc[0], 2),
        "monthly_sales": monthly_sales,
        "product_sales": product_sales,
        "region_sales": region_sales,
    }


def create_visualizations(df: pd.DataFrame, summary: dict) -> None:
    VISUALIZATION_DIR.mkdir(exist_ok=True)

    product_sales = summary["product_sales"]
    fig, ax = plt.subplots(figsize=(10, 6))
    product_sales.plot(kind="bar", color=["#4C78A8", "#F58518", "#54A24B", "#E45756", "#72B7B2"], ax=ax)
    ax.set_title("Total Sales by Product", fontsize=14, fontweight="bold")
    ax.set_xlabel("Product")
    ax.set_ylabel("Total Sales")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(VISUALIZATION_DIR / "product_sales_bar.png", dpi=300)
    plt.close(fig)

    monthly_sales = summary["monthly_sales"]
    fig, ax = plt.subplots(figsize=(10, 6))
    monthly_sales.plot(ax=ax, marker="o", linewidth=2, color="#2F5597")
    ax.set_title("Monthly Sales Trend", fontsize=14, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Sales")
    ax.grid(True, linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(VISUALIZATION_DIR / "monthly_sales_trend.png", dpi=300)
    plt.close(fig)


def write_report(summary: dict) -> Path:
    REPORT_DIR.mkdir(exist_ok=True)

    top_product = summary["top_product"]
    top_region = summary["top_region"]
    monthly_sales = summary["monthly_sales"]
    peak_month = monthly_sales.idxmax().strftime("%B %Y")
    peak_month_value = round(monthly_sales.max(), 2)

    report_lines = [
        "# E-commerce Sales Analysis Report",
        "",
        "This report uses the provided sales dataset to analyze sales performance across products, regions, and time.",
        "",
        "## Summary Metrics",
        "",
        f"- Total rows analyzed: {summary['rows']}",
        f"- Total revenue: {summary['total_revenue']}",
        f"- Total units sold: {summary['total_units']}",
        f"- Average sale value: {summary['average_sale_value']}",
        "",
        "## Key Findings",
        "",
        f"- The strongest product was {top_product} with total sales of {summary['top_product_sales']}.",
        f"- The leading region was {top_region} with total sales of {summary['top_region_sales']}.",
        f"- The highest sales month was {peak_month} with {peak_month_value} in revenue.",
        "",
        "## Insights",
        "",
        "- Sales performance is clearly driven by a small number of high-value products, which suggests that inventory planning should focus on these items.",
        "- Regional sales show that one market is consistently stronger, making it a priority for future marketing and expansion efforts.",
        "- The monthly trend indicates that revenue is not flat, so the business should review promotional timing and seasonal demand patterns.",
        "",
        "## Visualizations",
        "",
        "- Product sales bar chart: visualizations/product_sales_bar.png",
        "- Monthly sales trend line chart: visualizations/monthly_sales_trend.png",
    ]

    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    return REPORT_PATH


def main() -> None:
    try:
        df = load_and_validate_data(DATA_PATH)
        summary = analyze_sales(df)
        create_visualizations(df, summary)
        report_path = write_report(summary)

        print("Sales analysis completed successfully.")
        print(f"Report saved to: {report_path}")
        print(f"Charts saved to: {VISUALIZATION_DIR}")
        print(f"Total revenue: {summary['total_revenue']}")
        print(f"Top product: {summary['top_product']}")
        print(f"Top region: {summary['top_region']}")
    except Exception as exc:
        print(f"Analysis failed: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
