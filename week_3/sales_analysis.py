# Day 1: Setup & Load Data
import pandas as pd

df = pd.read_csv('sales_data.csv')

# Day 2: Explore Data
print(df.shape)
print(df.columns)
print(df.dtypes)
print(df.isnull().sum())

# Day 3: Clean Data
df = df.drop_duplicates()

mask = df['Total_Sales'].isnull() & df['Quantity'].notnull() & df['Price'].notnull()
df.loc[mask, 'Total_Sales'] = df.loc[mask, 'Quantity'] * df.loc[mask, 'Price']

df = df.dropna(subset=['Quantity', 'Price', 'Total_Sales'])

df['Quantity'] = df['Quantity'].astype(int)
df['Price'] = df['Price'].astype(float)
df['Total_Sales'] = df['Total_Sales'].astype(float)

# Day 4: Analyze Sales
total_revenue = df['Total_Sales'].sum()

revenue_by_product = df.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False)
best_product = revenue_by_product.index[0]
best_product_revenue = revenue_by_product.iloc[0]

avg_order_value = df['Total_Sales'].mean()

# Day 5: Create Report
report = []
report.append("SALES ANALYSIS REPORT")
report.append("=" * 100)
report.append(f"Total Revenue: ₹{total_revenue:,.2f}")
report.append(f"Best-Selling Product: {best_product} (₹{best_product_revenue:,.2f})")
report.append(f"Average Order Value: ₹{avg_order_value:,.2f}")
report.append("")
report.append("Revenue by Product:")
for product, rev in revenue_by_product.items():
    report.append(f"  {product}: ₹{rev:,.2f}")

report_text = "\n".join(report)
print(report_text)

with open('analysis_report.md', 'w', encoding='utf-8') as f:
    f.write(report_text)