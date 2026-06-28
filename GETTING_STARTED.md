# E-Commerce Sales Analytics Project - Getting Started

## Quick Start

### 1. Installation

```bash
git clone https://github.com/Akash82945/E-Commerce-Sales-Analytics.git
cd E-Commerce-Sales-Analytics
pip install -r requirements.txt
```

### 2. Generate Data

```bash
python data/data_generation.py
```

### 3. Run Analysis

```bash
jupyter notebook
```

Run notebooks in order: 01 → 02 → 03 → 04

## Project Structure

```
E-Commerce-Sales-Analytics/
├── README.md
├── requirements.txt
├── data/
│   ├── customers.csv
│   ├── orders.csv
│   ├── products.csv
│   └── data_generation.py
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_customer_segmentation.ipynb
│   └── 04_insights.ipynb
├── sql_queries/
│   ├── analysis_queries.sql
│   └── advanced_queries.sql
├── src/
│   ├── data_loader.py
│   └── analysis.py
└── reports/
    └── analysis_report.md
```

## Key Analyses

✅ Data Cleaning & Preprocessing  
✅ Exploratory Data Analysis  
✅ Customer Segmentation (RFM)  
✅ SQL Analytics  
✅ Business Insights & Recommendations  

## Key Findings

- **80/20 Rule**: Top 20% customers = 80% revenue
- **Seasonality**: Q4 = 35% annual revenue
- **Fulfillment**: 60% completion (opportunity: +$67.5K)
- **Geographic**: USA+UK = 55% of business

## Expected Growth

| Metric | Current | 12-Month |
|--------|---------|----------|
| Revenue | $450K | $675K |
| AOV | $450 | $520 |
| Retention | 65% | 80% |
| Fulfillment | 60% | 90% |

---

**Happy Analyzing!** 📊✨
