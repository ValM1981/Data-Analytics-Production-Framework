# 📊 Data Analytics Production Framework & E-Commerce Case Study

Welcome to my core Python portfolio project! This repository showcases a comprehensive, automated data analysis framework simulating a production-level data pipeline for a large e-commerce platform called **"ShopAnalytics"** (300,000+ data rows, including orders, web logs, and customer interactions).

Bypassing standard Jupyter Notebooks, this project is built entirely as a **modular Python package (.py scripts)** to adhere to enterprise-level software engineering standards, clean code architecture, and robust pipeline automation.

---

## 🔬 AI-Assisted Engineering & Development
The entire code logic, scripting, and pipeline optimizations within the `scripts/` directory were developed inside the **PyCharm IDE** leveraging **Claude AI as an engineering assistant**. 
*   **AI-Driven Optimization:** Utilized generative AI for rapid debugging, refactoring, and code performance acceleration.
*   **Prompt Engineering for Code:** Applied strict prompting to ensure mathematical correctness during raw data filtering and business metric algorithms.

---

## 🛠️ Advanced Tech Stack & Python Capabilities
*   **Core Languages & Environment:** Python 3.13+, Object-Oriented Programming (OOP), YAML configuration parsing.
*   **Data Engineering & ETL:** **Pandas 2.2+** and **NumPy** for advanced vector manipulations, data cleaning, and dataset merges.
*   **Database Operations:** Core integration with **SQLite** for relational querying, schema data filtering, and automated pipeline updates.
*   **Business Intelligence & Dashboards:** Developing interactive visualization components using **Plotly Dash** architectures.

---

## 📁 Project Architecture & Data Pipeline
The project follows a standard production layout to isolate raw ingestion from analytical solutions:
*   `main.py` — Single automated entry point managing the pipeline sequence (`generate`, `run`, `grade`, `dashboard`).
*   `data/raw/` & `data/cleaned/` — Decoupled data storage tracing data transformations from messy multi-format layers (CSV, JSON, Excel, SQLite) into production-ready analytical tables.
*   `scripts/` — **My core solution workspace**, including NumPy matrix tasks, Pandas aggregations, and visual storytelling modules.

---

## 🧹 The Data Cleaning & ETL Challenge
The pipeline generates simulated live business data embedded with severe anomalies to replicate real-world data issues. My code successfully resolves:
1.  **Structural Imbalance:** Handling missing records (`NaN`, `NULL`, blank spaces) and full/partial record duplications.
2.  **Type & Text Mutations:** Re-casting numerical features stored as text, converting mismatched date/time strings, and sanitizing string trailing spaces or casing errors.
3.  **Relational Integrity:** Resolving broken keys and non-existent IDs across the transaction graph (`Customers` -> `Orders` -> `Payments`).

---

## 📈 Business Scenario & Performance Metrics (ShopAnalytics)
Acting as the lead Data Analyst, I processed and analyzed a massive e-commerce relational dataset:
*   **Data Volume:** 30,000 customers | 250,000 orders | 5,000 products | 100,000 reviews | 250,000 payment logs.
*   **Analytical Objectives:** 
    *   Executed Exploratory Data Analysis (EDA) to map user behavioral patterns.
    *   Calculated critical commercial KPIs (Revenue growth metrics, Average Order Value - AOV, Churn Rates, User Engagement dynamics).
    *   Engineered automated interactive Sales and Marketing Dashboards via Plotly Dash to provide C-level executives with immediate insights.

---

## 🚀 Quick Start
To initialize the pipeline and experience the analytical dashboard environment:

```bash
# 1. Install required packages
pip install -r requirements.txt

# 2. Ingest and generate anomalous raw datasets
python main.py generate

# 3. Execute analytical modules (NumPy, Pandas, Visualizations)
python main.py run final_project

# 4. Fire up the Interactive BI Dashboards
python main.py dashboard sales
```

---

## 👩‍💻 Let's Connect!
I bridge the gap between rigorous mathematical logic (Ph.D. background) and production-grade Python engineering. If you are a recruiter, team lead, or tech explorer looking for a highly capable Junior Data Analyst, let’s talk:
*   **LinkedIn:**[linkedin.com/in/valentyna-matskevych-07389587](https://www.linkedin.com/in/valentyna-matskevych-07389587)
*   **Email:** matskevych.vt@gmail.com

