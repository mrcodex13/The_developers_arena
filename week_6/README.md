# 📊 Interactive Sales Dashboard

An interactive sales analytics project built with **Seaborn** (statistical plots) and **Plotly**
(interactive dashboard), analyzing `sales_data.csv` — 100 orders across 5 products and 4 regions
(Jan–Apr 2024).

## What's inside

| File / Folder        | Purpose                                                                                              |
| -------------------- | ---------------------------------------------------------------------------------------------------- |
| `dashboard.ipynb`    | Full walkthrough notebook, organized day-by-day (see guide below), with all charts rendered inline   |
| `dashboard.py`       | Standalone script — run it to regenerate every chart + the interactive HTML dashboard from scratch   |
| `visualizations/`    | All static PNG charts + the standalone animated Plotly HTML                                          |
| `dashboard.html`     | The full interactive dashboard (bar/box/line/heatmap + Region dropdown filter) — open in any browser |
| `requirements.txt`   | Python dependencies                                                                                  |
| `dashboard_demo.gif` | Quick animated preview cycling through the key charts                                                |
| `sales_data.csv`     | Source data                                                                                          |

## Setup

```bash
pip install -r requirements.txt
```

## Run it

```bash
python dashboard.py          # regenerates everything into visualizations/ + dashboard.html
jupyter notebook dashboard.ipynb   # or open the notebook directly
```

Then open `dashboard.html` in a browser for the interactive version.

## Chart types covered (5+ required)

1. **Line chart** — daily sales trend with 7-day rolling average
2. **Bar chart** — total revenue by product
3. **Box plot** — price distribution by product (with median annotations)
4. **Violin plot** — order quantity distribution by region
5. **Heatmaps** — numeric correlation matrix + Region × Product revenue matrix
6. **Scatter plot** — customer segmentation (spend tier) by quantity vs. total spend
7. **Interactive Plotly dashboard** — 2×2 linked panels (trend / bar / box / heatmap) with a
   Region dropdown filter and hover tooltips
8. **Animated bar chart** — cumulative revenue by product, animated month over month

## Color scheme

A single 5-color brand palette (navy `#1B2A4A`, teal `#2E9E9E`, coral `#F26B5B`, gold `#F2B33D`,
slate `#6C7A89`) is reused consistently across every Seaborn and Plotly chart, with the same
product → color mapping throughout, so the whole dashboard reads as one cohesive design rather
than a set of disconnected plots.

## Customer segmentation note

Each customer in this dataset has exactly one order, so "segmentation" here is done by
**spend tier** — orders are split into Low / Mid / High Value terciles by `Total_Sales` — rather
than by repeat-purchase behavior. If your own dataset has multiple orders per customer, swap in an
RFM (Recency/Frequency/Monetary) segmentation instead; the plotting code doesn't need to change,
just the `Spend_Tier` column logic in `load_data()`.

---

## 7-Day build guide (what was done, and why)

**Day 1 — Seaborn basics.** Set a shared color palette and `sns.set_theme()`; built the first
line and bar charts to get the data pipeline (load → group → plot) working.

**Day 2 — Statistical visualizations.** Box plot (price by product) and violin plot (quantity by
region) to see full distributions, not just averages; added median-value text annotations on the
box plot; added a scatter plot for customer segmentation.

**Day 3 — Heatmaps & correlation.** Built a numeric correlation matrix (`Quantity`, `Price`,
`Total_Sales`) and a custom Region × Product pivot-table heatmap.

**Day 4 — Multi-plot dashboard.** Combined four of the above into a single 2×2 `plt.subplots()`
grid with one consistent title, palette, and layout — `visualizations/day4_dashboard_grid.png`.

**Day 5 — Interactive visualizations.** Rebuilt the key charts in Plotly for hover tooltips, and
added an animated cumulative-revenue-by-product bar chart (`day5_animated_trend.html`).

**Day 6 — Dashboard integration.** Combined everything into one Plotly `make_subplots()` layout
(trend / bar / box / heatmap) with a working **Region dropdown filter** that updates all four
panels at once — `dashboard.html`.

**Day 7 — Polish & presentation.** Applied one cohesive color scheme everywhere, wrote this
README, and generated `dashboard_demo.gif` as a lightweight preview for anyone who can't open the
HTML file directly (e.g. viewing the repo on GitHub).

---

## Suggested GitHub repo structure

```
sales-dashboard/
├── dashboard.ipynb
├── dashboard.py
├── dashboard_demo.gif
├── requirements.txt
├── sales_data.csv
├── README.md
└── visualizations/
    ├── day1_sales_trend.png
    ├── day1_bar_by_product.png
    ├── day2_box_price_by_product.png
    ├── day2_violin_quantity_by_region.png
    ├── day2_customer_segmentation_scatter.png
    ├── day3_correlation_heatmap.png
    ├── day3_region_product_heatmap.png
    ├── day4_dashboard_grid.png
    └── day5_animated_trend.html
```
