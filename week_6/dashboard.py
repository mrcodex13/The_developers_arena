"""
Interactive Sales Dashboard
===========================
Analyzes sales_data.csv and produces:
  - Seaborn statistical plots (box, violin, heatmap, etc.) saved to visualizations/
  - A 2x2 coordinated static dashboard (visualizations/day4_dashboard_grid.png)
  - A fully interactive Plotly dashboard (dashboard.html) with dropdown filters,
    hover tooltips, and an animation over time

Run with:  python dashboard.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os

# ---------------------------------------------------------------------------
# 0. Setup: cohesive color scheme + folders
# ---------------------------------------------------------------------------
OUT_DIR = "visualizations"
os.makedirs(OUT_DIR, exist_ok=True)

# Brand palette - used consistently across every Seaborn AND Plotly chart
PALETTE = {
    "navy": "#1B2A4A",
    "teal": "#2E9E9E",
    "coral": "#F26B5B",
    "gold": "#F2B33D",
    "slate": "#6C7A89",
}
PALETTE_LIST = list(PALETTE.values())
PRODUCT_COLORS = {}  # filled in once we know the products

sns.set_theme(style="whitegrid", palette=PALETTE_LIST)
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "#D9DEE4",
    "axes.titleweight": "bold",
    "axes.titlesize": 14,
    "axes.titlecolor": PALETTE["navy"],
    "font.family": "sans-serif",
})

PLOTLY_TEMPLATE = "plotly_white"


# ---------------------------------------------------------------------------
# 1. Load & prepare data
# ---------------------------------------------------------------------------
def load_data(path="sales_data.csv"):
    df = pd.read_csv(path, parse_dates=["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["Week"] = df["Date"].dt.to_period("W").astype(str)

    # Customer segmentation by spend (each customer has one order in this
    # dataset, so we segment on order value into tiers)
    df["Spend_Tier"] = pd.qcut(
        df["Total_Sales"], q=3, labels=["Low Value", "Mid Value", "High Value"]
    )

    global PRODUCT_COLORS
    products = sorted(df["Product"].unique())
    PRODUCT_COLORS = {p: PALETTE_LIST[i % len(PALETTE_LIST)] for i, p in enumerate(products)}

    return df


# ---------------------------------------------------------------------------
# DAY 1-2: Seaborn basics + statistical visualizations
# ---------------------------------------------------------------------------
def plot_sales_trend(df):
    """Line chart: daily sales trend with rolling average."""
    daily = df.groupby("Date", as_index=False)["Total_Sales"].sum()
    daily["Rolling_7d"] = daily["Total_Sales"].rolling(7, min_periods=1).mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=daily, x="Date", y="Total_Sales", color=PALETTE["slate"],
                 alpha=0.5, label="Daily Sales", ax=ax)
    sns.lineplot(data=daily, x="Date", y="Rolling_7d", color=PALETTE["navy"],
                 linewidth=2.5, label="7-Day Avg", ax=ax)
    ax.set_title("Daily Sales Trend")
    ax.set_ylabel("Total Sales ($)")
    ax.set_xlabel("Date")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/day1_sales_trend.png", dpi=150)
    plt.close()


def plot_bar_by_product(df):
    """Bar chart: total revenue by product."""
    totals = df.groupby("Product", as_index=False)["Total_Sales"].sum().sort_values(
        "Total_Sales", ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=totals, x="Product", y="Total_Sales",
                hue="Product", palette=PRODUCT_COLORS, legend=False, ax=ax)
    for i, v in enumerate(totals["Total_Sales"]):
        ax.text(i, v, f"${v:,.0f}", ha="center", va="bottom", fontsize=9)
    ax.set_title("Total Revenue by Product")
    ax.set_ylabel("Total Sales ($)")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/day1_bar_by_product.png", dpi=150)
    plt.close()


def plot_box_price_by_category(df):
    """Box plot with statistical annotation (median labels)."""
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x="Product", y="Price", hue="Product",
                palette=PRODUCT_COLORS, legend=False, ax=ax)
    medians = df.groupby("Product")["Price"].median()
    for i, product in enumerate(sorted(df["Product"].unique())):
        ax.text(i, medians[product], f"med: ${medians[product]:,.0f}",
                ha="center", va="bottom", fontsize=8, color=PALETTE["navy"])
    ax.set_title("Price Distribution by Product")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/day2_box_price_by_product.png", dpi=150)
    plt.close()


def plot_violin_quantity_by_region(df):
    """Violin plot: order quantity distribution by region."""
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.violinplot(data=df, x="Region", y="Quantity", hue="Region",
                    palette=PALETTE_LIST, legend=False, ax=ax)
    ax.set_title("Order Quantity Distribution by Region")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/day2_violin_quantity_by_region.png", dpi=150)
    plt.close()


# ---------------------------------------------------------------------------
# DAY 3: Heatmaps & correlation
# ---------------------------------------------------------------------------
def plot_correlation_heatmap(df):
    corr = df[["Quantity", "Price", "Total_Sales"]].corr()
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
                square=True, linewidths=0.5, ax=ax)
    ax.set_title("Correlation Matrix")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/day3_correlation_heatmap.png", dpi=150)
    plt.close()


def plot_region_product_heatmap(df):
    """Custom heatmap: total sales by Region x Product."""
    pivot = df.pivot_table(values="Total_Sales", index="Region",
                            columns="Product", aggfunc="sum", fill_value=0)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", linewidths=0.5, ax=ax)
    ax.set_title("Total Sales: Region vs Product")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/day3_region_product_heatmap.png", dpi=150)
    plt.close()


# ---------------------------------------------------------------------------
# DAY 4: 2x2 coordinated subplot dashboard grid
# ---------------------------------------------------------------------------
def plot_2x2_dashboard(df):
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    fig.suptitle("Sales Performance Overview", fontsize=18, fontweight="bold",
                 color=PALETTE["navy"])

    # Top-left: revenue by product
    totals = df.groupby("Product", as_index=False)["Total_Sales"].sum().sort_values(
        "Total_Sales", ascending=False)
    sns.barplot(data=totals, x="Product", y="Total_Sales", hue="Product",
                palette=PRODUCT_COLORS, legend=False, ax=axes[0, 0])
    axes[0, 0].set_title("Revenue by Product")

    # Top-right: sales trend
    daily = df.groupby("Date", as_index=False)["Total_Sales"].sum()
    sns.lineplot(data=daily, x="Date", y="Total_Sales", color=PALETTE["teal"], ax=axes[0, 1])
    axes[0, 1].set_title("Daily Sales Trend")
    axes[0, 1].tick_params(axis="x", rotation=30)

    # Bottom-left: box plot of price by product
    sns.boxplot(data=df, x="Product", y="Price", hue="Product",
                palette=PRODUCT_COLORS, legend=False, ax=axes[1, 0])
    axes[1, 0].set_title("Price Distribution by Product")

    # Bottom-right: customer spend tier pie
    tier_counts = df["Spend_Tier"].value_counts()
    axes[1, 1].pie(tier_counts.values, labels=tier_counts.index, autopct="%1.0f%%",
                   colors=[PALETTE["coral"], PALETTE["gold"], PALETTE["navy"]],
                   startangle=90, wedgeprops={"edgecolor": "white"})
    axes[1, 1].set_title("Customers by Spend Tier")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f"{OUT_DIR}/day4_dashboard_grid.png", dpi=150)
    plt.close()


# ---------------------------------------------------------------------------
# Customer segmentation scatter (extra statistical view)
# ---------------------------------------------------------------------------
def plot_customer_segmentation(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=df, x="Quantity", y="Total_Sales", hue="Spend_Tier",
                     palette=[PALETTE["coral"], PALETTE["gold"], PALETTE["navy"]],
                     s=80, alpha=0.8, ax=ax)
    ax.set_title("Customer Segmentation: Quantity vs Total Spend")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/day2_customer_segmentation_scatter.png", dpi=150)
    plt.close()


# ---------------------------------------------------------------------------
# DAY 5-6: Interactive Plotly dashboard
# ---------------------------------------------------------------------------
def build_interactive_dashboard(df, out_html="dashboard.html"):
    products = sorted(df["Product"].unique())
    regions = sorted(df["Region"].unique())

    daily_all = df.groupby("Date", as_index=False)["Total_Sales"].sum()

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Sales Trend Over Time", "Revenue by Product",
            "Price Distribution by Product", "Sales by Region & Product (Heatmap)"
        ),
        specs=[[{"type": "scatter"}, {"type": "bar"}],
               [{"type": "box"}, {"type": "heatmap"}]],
        vertical_spacing=0.15, horizontal_spacing=0.12,
    )

    # --- Panel 1: sales trend (all data, always visible trace 0) ---
    fig.add_trace(
        go.Scatter(x=daily_all["Date"], y=daily_all["Total_Sales"], mode="lines+markers",
                   name="Total Sales", line=dict(color=PALETTE["navy"], width=2),
                   hovertemplate="Date: %{x}<br>Sales: $%{y:,.0f}<extra></extra>"),
        row=1, col=1,
    )

    # --- Panel 2: revenue by product (bar) ---
    totals = df.groupby("Product", as_index=False)["Total_Sales"].sum().sort_values(
        "Total_Sales", ascending=False)
    fig.add_trace(
        go.Bar(x=totals["Product"], y=totals["Total_Sales"],
               marker_color=[PRODUCT_COLORS[p] for p in totals["Product"]],
               name="Revenue",
               hovertemplate="Product: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>"),
        row=1, col=2,
    )

    # --- Panel 3: box plot of price by product ---
    for p in products:
        sub = df[df["Product"] == p]
        fig.add_trace(
            go.Box(y=sub["Price"], name=p, marker_color=PRODUCT_COLORS[p],
                   hovertemplate="Price: $%{y:,.0f}<extra></extra>"),
            row=2, col=1,
        )

    # --- Panel 4: heatmap of region x product total sales ---
    pivot = df.pivot_table(values="Total_Sales", index="Region", columns="Product",
                            aggfunc="sum", fill_value=0)
    fig.add_trace(
        go.Heatmap(z=pivot.values, x=pivot.columns, y=pivot.index,
                   colorscale="Tealrose",
                   hovertemplate="Region: %{y}<br>Product: %{x}<br>Sales: $%{z:,.0f}<extra></extra>"),
        row=2, col=2,
    )

    # --- Dropdown: filter everything by Region ---
    region_options = ["All Regions"] + regions
    buttons = []
    for reg in region_options:
        sub = df if reg == "All Regions" else df[df["Region"] == reg]

        daily = sub.groupby("Date", as_index=False)["Total_Sales"].sum()
        totals_r = sub.groupby("Product")["Total_Sales"].sum().reindex(
            totals["Product"].tolist(), fill_value=0.0)
        pivot_r = sub.pivot_table(values="Total_Sales", index="Region", columns="Product",
                                   aggfunc="sum", fill_value=0.0)
        pivot_r = pivot_r.reindex(columns=pivot.columns.tolist(), fill_value=0.0)
        pivot_r = pivot_r.reindex(index=pivot.index.tolist(), fill_value=0.0)

        box_ys = [sub[sub["Product"] == p]["Price"].tolist() for p in products]

        buttons.append(dict(
            label=reg,
            method="update",
            args=[{
                "x": [daily["Date"]] + [totals["Product"]] + [None] * len(products) + [pivot.columns],
                "y": [daily["Total_Sales"]] + [totals_r.values] + box_ys + [pivot_r.index],
                "z": [None, None] + [None] * len(products) + [pivot_r.values],
            }],
        ))

    fig.update_layout(
        updatemenus=[dict(
            buttons=buttons, direction="down", x=1.0, xanchor="right",
            y=1.15, yanchor="top", showactive=True,
            bgcolor="white", bordercolor=PALETTE["slate"],
        )],
        annotations=[dict(text="Filter by Region:", x=1.0, xref="paper", y=1.20,
                           yref="paper", showarrow=False, xanchor="right")],
        title=dict(text="Interactive Sales Dashboard", font=dict(size=22, color=PALETTE["navy"])),
        template=PLOTLY_TEMPLATE,
        height=850, width=1200,
        showlegend=False,
        margin=dict(t=140),
    )
    fig.update_yaxes(title_text="Total Sales ($)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($)", row=1, col=2)
    fig.update_yaxes(title_text="Price ($)", row=2, col=1)

    fig.write_html(out_html, include_plotlyjs="cdn")
    print(f"Interactive dashboard saved to {out_html}")
    return fig


def build_animated_trend(df, out_html="visualizations/day5_animated_trend.html"):
    """Animated bar chart race: cumulative revenue by product over months."""
    monthly = df.groupby(["Month", "Product"], as_index=False)["Total_Sales"].sum()
    monthly = monthly.sort_values("Month")
    monthly["Cumulative"] = monthly.groupby("Product")["Total_Sales"].cumsum()

    fig = px.bar(
        monthly, x="Product", y="Cumulative", color="Product",
        color_discrete_map=PRODUCT_COLORS, animation_frame="Month",
        range_y=[0, monthly["Cumulative"].max() * 1.1],
        title="Cumulative Revenue by Product Over Time",
        template=PLOTLY_TEMPLATE,
    )
    fig.update_layout(showlegend=False, height=550, width=850)
    fig.write_html(out_html, include_plotlyjs="cdn")
    print(f"Animated chart saved to {out_html}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    df = load_data("sales_data.csv")

    print("Generating Seaborn statistical visualizations...")
    plot_sales_trend(df)
    plot_bar_by_product(df)
    plot_box_price_by_category(df)
    plot_violin_quantity_by_region(df)
    plot_customer_segmentation(df)

    print("Generating heatmaps...")
    plot_correlation_heatmap(df)
    plot_region_product_heatmap(df)

    print("Building 2x2 coordinated dashboard grid...")
    plot_2x2_dashboard(df)

    print("Building interactive Plotly dashboard...")
    build_interactive_dashboard(df, out_html="dashboard.html")
    build_animated_trend(df)

    print(f"\nAll static charts saved in '{OUT_DIR}/'.")
    print("Open 'dashboard.html' in a browser for the interactive dashboard.")


if __name__ == "__main__":
    main()