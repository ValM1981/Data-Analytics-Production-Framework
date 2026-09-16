"""
Pandas Tasks — Навчальний скрипт для практики Pandas.

Теми:
1. Читання файлів та DataFrame
2. Фільтрація та сортування
3. groupby та агрегація
4. merge та join
5. pivot_tables
6. Робота з датами
7. String методи
8. Пропущені значення
9. Дублікати
10. apply та lambda

Інструкція:
- Заповніть код після # TODO:
- Використовуйте pandas та прочитані дані
"""
import pandas as pd
import numpy as np
from pathlib import Path

# Завантажуємо дані
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def load_data():
    """Завантажує всі дані для завдань."""
    customers = pd.read_csv(DATA_DIR / "customers.csv")
    orders = pd.read_csv(DATA_DIR / "orders.csv")
    products = pd.read_csv(DATA_DIR / "products.csv")
    payments = pd.read_csv(DATA_DIR / "payments.csv")
    reviews = pd.read_csv(DATA_DIR / "reviews.csv")
    return customers, orders, products, payments, reviews


customers, orders, products, payments, reviews = load_data()

# =========================================
# Завдання 1: Базовий аналіз DataFrame
# =========================================
# Виведіть: перші 10 рядків, info(), describe(), shape, колонки
# для customers DataFrame
# TODO:
customers_head = customers.head(10)
customers_info = customers.info()
customers_shape = customers.shape
customers_columns = customers.columns.tolist()
print(f"Shape: {customers_shape}")
print(f"Колонки: {customers_columns.tolist()}")

# =========================================
# Завдання 2: Фільтрація та сортування
# =========================================
# Знайдіть всі замовлення з status = "delivered" та total_amount > 1000,
# відсортуйте за датою замовлення (новіші перші)
# TODO:
delivered_high_value = orders[
    (orders["status"] == "delivered") & (orders["total_amount"] > 1000)
].sort_values("order_date", ascending=False)

# =========================================
# Завдання 3: Groupby агрегація
# =========================================
# Порахуйте для кожної категорії товарів:
# - середню ціну
# - медіанну ціну
# - кількість товарів
# - мінімальну та максимальну ціну
# TODO:
category_stats = products.groupby("category")["price"].agg(
    avg_price="mean",
    median_price="median",
    count="count",
    min_price="min",
    max_price="max"
).reset_index()

# =========================================
# Завдання 4: Merge (об'єднання таблиць)
# =========================================
# Об'єднайте orders та customers, щоб отримати замовлення
# з інформацією про клієнта (city, age)
# Який клієнт зробив найбільше замовлень?
# TODO:
orders_with_customers = pd.merge(
    orders, customers, on="customer_id", how="left"
)
top_customer = (
    orders_with_customers.groupby("customer_id")
    .size()
    .idxmax()
)

# =========================================
# Завдання 5: Pivot table
# =========================================
# Створіть pivot_table: рядки = city, стовпці = status,
# значення = кількість замовлень, агрегація = count
# TODO:
pivot_status = pd.pivot_table(
    orders_with_customers,
    index="city",
    columns="status",
    values="order_id",
    aggfunc="count",
    fill_value=0
)

# =========================================
# Завдання 6: Робота з датами
# =========================================
# Додайте колонки: year, month, day_of_week до orders
# Знайдіть місяць з найбільшою кількістю замовлень
# TODO:
orders_with_date = orders.copy()
orders_with_date["order_date"] = pd.to_datetime(orders_with_date["order_date"])
orders_with_date["year"] = orders_with_date["order_date"].dt.year
orders_with_date["month"] = orders_with_date["order_date"].dt.month
orders_with_date["day_of_week"] = orders_with_date["order_date"].dt.dayofweek
busiest_month = orders_with_date.groupby(["year", "month"]).size().idxmax()

# =========================================
# Завдання 7: String методи
# =========================================
# В customers знайдіть:
# - кількість клієнтів з email на gmail.com
# - клієнтів, чиє ім'я починається на "A"
# - домени email (частина після @) з частотою
# TODO:
gmail_count = customers["email"].str.contains("@gmail.com", case=False).sum()
names_starting_a = customers[customers["name"].str.startswith("A", na=False)]
email_domains = customers["email"].str.split("@").str[1].value_counts()

# =========================================
# Завдання 8: Пропущені значення
# =========================================
# В products знайдіть:
# - відсоток пропусків у кожній колонці
# - заповніть пропуски в brand на "Unknown"
# - заповніть пропуски в rating на середній рейтинг
# TODO:
null_pct = products.isnull().mean() * 100
products_filled = products.copy()
products_filled["brand"] = products_filled["brand"].fillna("Unknown")
products_filled["rating"] = products_filled["rating"].fillna(products_filled["rating"].mean())

# =========================================
# Завдання 9: Дублікати
# =========================================
# Знайдіть та видаліть дублікати:
# - скільки повних дублікатів у orders?
# - скільки часткових (однаковий order_id)?
# TODO:
full_dupes = orders.duplicated().sum()
partial_dupes = orders.duplicated(subset=["order_id"]).sum()
orders_deduped = orders.drop_duplicates()

# =========================================
# Завдання 10: Apply та Lambda
# =========================================
# Створіть колонку "price_category" в products:
# - "budget": price < 500
# - "mid": price 500-5000
# - "premium": price > 5000
# Використайте apply з lambda функцією
# TODO:
products_with_category = products.copy()
products_with_category["price_category"] = products_with_category["price"].apply(
    lambda p: "budget" if p < 500 else ("premium" if p > 5000 else "mid")
)


if __name__ == "__main__":
    print("=" * 50)
    print("Pandas Tasks")
    print("=" * 50)
    print("Відкрийте цей файл у PyCharm та заповніть TODO")
    print("Після виконання запустіть: python main.py grade")
