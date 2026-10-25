# Olist E-commerce Business Analytics

## Project Overview
An end-to-end business analytics project using the Olist Brazilian e-commerce dataset to analyze sales performance, product categories, and delivery operations. The goal is to generate actionable business insights using data analysis and visualization tools.

## Tools & Technologies
- **Python:** Pandas for data cleaning, transformation, and exploratory data analysis
- **SQL:** SQL queries using DuckDB to analyze data and validate key performance indicators
- **Power BI:** Interactive dashboards and business performance visualization

## Business Questions
- How do sales trends change over time?
- Which product categories contribute most to sales?
- What insights can delivery performance provide about operational efficiency?

## Project Workflow
1. Analyzed and explored the dataset using Python and Pandas.
2. Used SQL and DuckDB to query data and validate key metrics.
3. Built a Power BI dashboard to visualize business performance.

## Key Skills Demonstrated
Data cleaning, exploratory data analysis, SQL querying, KPI validation, data visualization, and business-oriented analytical thinking.

## Project Status
Portfolio project in progress. Additional insights, dashboard screenshots, and detailed findings will be added as the project documentation develops.
## Power BI Dashboard

![Olist Power BI Dashboard](olist-dashboard.PNG)

## Key Business Insights

### 1. Monthly Sales Trend
- Observed substantial growth in monthly order volume and payment value from late 2016 through 2017, continuing into most of 2018.
- November 2017 recorded the highest monthly payment value in the supplied results, at approximately **R$1.19 million**, with 7,544 orders.
- Sales and order volume dropped sharply in September and October 2018. October contained only 4 orders and approximately R$589.67 in payments.
- **Data limitation:** The dataset ends on 17 October 2018, making October a partial month. September's unusually low order volume also warrants investigation before interpreting the decline as a genuine business trend.

### 2. Product Category Performance
- **Health & Beauty** generated the highest total sales among the 10 categories shown, at approximately **R$1.26 million**, across 9,670 items.
- **Watches & Gifts** ranked second by total sales, generating approximately **R$1.21 million**, despite selling fewer items (5,991).
- **Bed, Bath & Table** recorded the highest item volume, with 11,115 items sold and approximately R$1.04 million in sales.
- These findings highlight differences between revenue performance and sales volume. Category-level pricing, product demand, and sales strategies can be explored further to identify growth opportunities.

### 3. Delivery Performance and Operational Efficiency
- Analyzed 96,478 delivered orders, of which 96,470 had complete delivery dates; 8 orders were excluded because delivery dates were missing.
- Average delivery time was **12.56 days**.
- **6,534 orders (6.77%)** were delivered late, while **89,936 orders (93.23%)** were delivered on time or early.
- Although most orders met their estimated delivery dates, late deliveries remain an opportunity for operational improvement. Monitoring late-delivery rates and investigating the causes of delays could help improve delivery reliability and customer experience.
