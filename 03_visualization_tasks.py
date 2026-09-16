"""
Visualization Tasks — Навчальний скрипт для візуалізації даних.

Теми:
1. Line chart (Matplotlib)
2. Bar chart (Matplotlib)
3. Scatter plot
4. Histogram
5. Boxplot
6. Heatmap (Seaborn)
7. Subplots
8. Pairplot (Seaborn)
9. Countplot
10. Regression plot

Інструкція:
- Заповніть код після # TODO:
- Графіки зберігаються в reports/
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # для роботи без GUI
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Шляхи
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Завантажуємо дані
customers = pd.read_csv(DATA_DIR / "customers.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")
products = pd.read_csv(DATA_DIR / "products.csv")
reviews = pd.read_csv(DATA_DIR / "reviews.csv")


# =========================================
# Завдання 1: Line chart — продажі по місяцях
# =========================================
# Побудуйте лінійний графік кількості замовлень по місяцях.
# Збережіть як reports/line_sales.png
# TODO:
def task1_line_chart():
    fig, ax = plt.subplots(figsize=(12, 6))
    # Ваш код тут
    orders["order_date"] = pd.to_datetime(orders["order_date"], format="mixed", errors="coerce")
    monthly_orders = orders.set_index("order_date").resample("ME").size()
    ax.plot(monthly_orders.index, monthly_orders.values, marker="o", linewidth=2)
    plt.title("Продажі по місяцях")
    plt.xlabel("Місяць")
    plt.ylabel("Кількість замовлень")
    plt.grid(True, alpha=0.3)
    plt.savefig(REPORTS_DIR / "line_sales.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("✓ line_sales.png збережено")


# =========================================
# Завдання 2: Bar chart — продажі по категоріях
# =========================================
# Побудуйте стовпчикову діаграму кількості товарів за категоріями.
# Збережіть як reports/bar_categories.png
# TODO:
def task2_bar_chart():
    fig, ax = plt.subplots(figsize=(10, 6))
    # Ваш код тут
    category_counts = products["category"].value_counts()
    ax.bar(category_counts.index, category_counts.values, color="steelblue")
    plt.title("Кількість товарів за категоріями")
    plt.xlabel("Категорія")
    plt.ylabel("Кількість")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "bar_categories.png", dpi=100)
    plt.close()
    print("✓ bar_categories.png збережено")


# =========================================
# Завдання 3: Scatter plot — ціна vs рейтинг
# =========================================
# Побудуйте scatter plot: ціна товару (x) vs рейтинг (y).
# Додайте колір за категорією.
# Збережіть як reports/scatter_price_rating.png
# TODO:
def task3_scatter():
    fig, ax = plt.subplots(figsize=(10, 8))
    # Ваш код тут
    categories = products["category"].unique()
    colors = plt.cm.tab10(range(len(categories)))
    for cat, color in zip(categories, colors):
        mask = products["category"] == cat
        ax.scatter(
            products.loc[mask, "price"],
            products.loc[mask, "rating"],
            label=cat, color=color, alpha=0.5, s=30
        )
    plt.title("Ціна vs Рейтинг товарів")
    plt.xlabel("Ціна")
    plt.ylabel("Рейтинг")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "scatter_price_rating.png", dpi=100)
    plt.close()
    print("✓ scatter_price_rating.png збережено")


# =========================================
# Завдання 4: Histogram — розподіл цін
# =========================================
# Побудуйте гістограму розподілу цін товарів (30 бінів).
# Збережіть як reports/hist_prices.png
# TODO:
def task4_histogram():
    fig, ax = plt.subplots(figsize=(10, 6))
    # Ваш код тут
    ax.hist(products["price"].dropna(), bins=30, color="steelblue", edgecolor="white", alpha=0.7)
    plt.title("Розподіл цін товарів")
    plt.xlabel("Ціна")
    plt.ylabel("Частота")
    plt.grid(True, alpha=0.3)
    plt.savefig(REPORTS_DIR / "hist_prices.png", dpi=100)
    plt.close()
    print("✓ hist_prices.png збережено")


# =========================================
# Завдання 5: Boxplot — ціни за категоріями
# =========================================
# Побудуйте boxplot цін товарів у розрізі категорій.
# Збережіть як reports/boxplot_prices.png
# TODO:
def task5_boxplot():
    fig, ax = plt.subplots(figsize=(12, 6))
    # Ваш код тут
    sns.boxplot(data=products, x="category", y="price", ax=ax, palette="Set3")
    plt.title("Розподіл цін за категоріями")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "boxplot_prices.png", dpi=100)
    plt.close()
    print("✓ boxplot_prices.png збережено")


# =========================================
# Завдання 6: Heatmap — кореляція
# =========================================
# Побудуйте теплову карту кореляції числових колонок orders.
# Збережіть як reports/heatmap_correlation.png
# TODO:
def task6_heatmap():
    fig, ax = plt.subplots(figsize=(10, 8))
    # Ваш код тут
    numeric_cols = orders.select_dtypes(include=[np.number])
    corr = numeric_cols.corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
    plt.title("Кореляція числових змінних")
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "heatmap_correlation.png", dpi=100)
    plt.close()
    print("✓ heatmap_correlation.png збережено")


# =========================================
# Завдання 7: Subplots — 4 графіки разом
# =========================================
# Створіть 4 subplots (2x2):
# - top-left: line chart продажів
# - top-right: bar chart категорій
# - bottom-left: scatter ціна vs рейтинг
# - bottom-right: histogram цін
# Збережіть як reports/subplots_dashboard.png
# TODO:
def task7_subplots():
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    # Ваш код тут
    # Top-left: Line chart продажів по місяцях
    orders["order_date"] = pd.to_datetime(orders["order_date"], format="mixed", errors="coerce")
    monthly = orders.set_index("order_date").resample("ME").size()
    axes[0, 0].plot(monthly.index, monthly.values, marker="o")
    axes[0, 0].set_title("Продажі по місяцях")
    axes[0, 0].grid(True, alpha=0.3)

    # Top-right: Bar chart категорій
    cat_counts = products["category"].value_counts()
    axes[0, 1].bar(cat_counts.index, cat_counts.values, color="steelblue")
    axes[0, 1].set_title("Товари за категоріями")
    axes[0, 1].tick_params(axis="x", rotation=45)

    # Bottom-left: Scatter ціна vs рейтинг
    axes[1, 0].scatter(products["price"], products["rating"], alpha=0.3, s=10)
    axes[1, 0].set_title("Ціна vs Рейтинг")
    axes[1, 0].set_xlabel("Ціна")
    axes[1, 0].set_ylabel("Рейтинг")

    # Bottom-right: Histogram цін
    axes[1, 1].hist(products["price"].dropna(), bins=30, color="steelblue", edgecolor="white")
    axes[1, 1].set_title("Розподіл цін")
    axes[1, 1].set_xlabel("Ціна")

    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "subplots_dashboard.png", dpi=100)
    plt.close()
    print("✓ subplots_dashboard.png збережено")


# =========================================
# Завдання 8: Pairplot (Seaborn)
# =========================================
# Побудуйте pairplot для числових колонок customers
# (age) та orders (quantity, total_amount) — об'єднайте їх
# Збережіть як reports/pairplot.png
# TODO:
def task8_pairplot():
    # Ваш код тут
    merged = pd.merge(
        orders[["customer_id", "quantity", "total_amount"]],
        customers[["customer_id", "age", "city"]],
        on="customer_id"
    )
    pairplot_fig = sns.pairplot(
        merged, vars=["age", "quantity", "total_amount"], diag_kind="hist", height=3
    )
    pairplot_fig.savefig(REPORTS_DIR / "pairplot.png", dpi=100)
    plt.close()
    print("✓ pairplot.png збережено")


# =========================================
# Завдання 9: Countplot — статуси замовлень
# =========================================
# Побудуйте countplot статусів замовлень.
# Збережіть як reports/countplot_status.png
# TODO:
def task9_countplot():
    fig, ax = plt.subplots(figsize=(10, 6))
    # Ваш код тут
    sns.countplot(data=orders, x="status", ax=ax, palette="Set2",
                  order=orders["status"].value_counts().index)
    plt.title("Розподіл статусів замовлень")
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "countplot_status.png", dpi=100)
    plt.close()
    print("✓ countplot_status.png збережено")


# =========================================
# Завдання 10: Regression plot
# =========================================
# Побудуйте regplot: залежність total_amount від quantity
# (як змінюється сума замовлення від кількості товарів)
# Збережіть як reports/regplot_amount_qty.png
# TODO:
def task10_regplot():
    fig, ax = plt.subplots(figsize=(10, 6))
    # Ваш код тут
    sns.regplot(data=orders, x="quantity", y="total_amount", ax=ax,
                scatter_kws={"alpha": 0.3, "s": 5}, line_kws={"color": "red"})
    plt.title("Залежність суми від кількості товарів")
    plt.xlabel("Кількість")
    plt.ylabel("Загальна сума")
    plt.savefig(REPORTS_DIR / "regplot_amount_qty.png", dpi=100)
    plt.close()
    print("✓ regplot_amount_qty.png збережено")


if __name__ == "__main__":
    print("=" * 50)
    print("Visualization Tasks")
    print("=" * 50)
    print("Відкрийте кожну функцію та заповніть TODO")
    print()
    print("1. Line chart")
    print("2. Bar chart")
    print("3. Scatter plot")
    print("4. Histogram")
    print("5. Boxplot")
    print("6. Heatmap")
    print("7. Subplots")
    print("8. Pairplot")
    print("9. Countplot")
    print("10. Regression plot")
    print()
    print("Запустіть функції окремо або всі разом:")
    print("  task1_line_chart()")
    print("  ...")
