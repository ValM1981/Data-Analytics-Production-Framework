"""
Фінальний проєкт: Junior Data Analyst Interview Case.

Бізнес-сценарій:
Ви — Data Analyst в компанії "ShopAnalytics" (інтернет-магазин).
CEO просить вас проаналізувати ефективність бізнесу за 2024-2025 роки.

Що потрібно зробити:
1. Очистити дані (знайти та виправити проблеми)
2. Проаналізувати ключові метрики
3. Написати SQL запити
4. Побудувати візуалізації
5. Створити дашборд
6. Зробити бізнес-висновки

Формат здачі:
- Цей файл із заповненим кодом
- Графіки в reports/
- Висновки в кінці файлу
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sqlite3

# Шляхи
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"
CLEANED_DIR = BASE_DIR / "data" / "cleaned"
DB_PATH = BASE_DIR / "data" / "database" / "analytics.db"
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# =========================================
# 1. ОЧИСТКА ДАНИХ
# =========================================

def load_and_clean_data():
    """
    Завантажте та очистіть дані.
    Поверніть словник з очищеними DataFrame.

    Кроки:
    - Завантажте customers.csv, orders.csv, products.csv, reviews.csv
    - Видаліть дублікати
    - Виправте типи даних
    - Заповніть/видаліть пропуски
    - Виправте формати дат
    - Видаліть аномалії
    """
    # TODO: завантажте дані
    customers = pd.read_csv(DATA_DIR / "customers.csv")
    orders = pd.read_csv(DATA_DIR / "orders.csv")
    products = pd.read_csv(DATA_DIR / "products.csv")
    reviews = pd.read_csv(DATA_DIR / "reviews.csv")

    # TODO: очистіть дані

    # --- CUSTOMERS ---
    # Видаляємо дублікати
    customers = customers.drop_duplicates()
    # Заповнюємо пропуски
    customers["first_name"] = customers["first_name"].fillna("Unknown")
    customers["last_name"] = customers["last_name"].fillna("Unknown")
    customers["email"] = customers["email"].fillna("unknown@email.com")
    customers["city"] = customers["city"].fillna("Unknown")
    customers["age"] = customers["age"].fillna(customers["age"].median()).astype(int)
    customers["registration_date"] = pd.to_datetime(
        customers["registration_date"], format="mixed", errors="coerce"
    )

    # --- ORDERS ---
    orders = orders.drop_duplicates()
    # Конвертуємо дати
    orders["order_date"] = pd.to_datetime(orders["order_date"], format="mixed", errors="coerce")
    # Видаляємо рядки з невалідними датами
    orders = orders.dropna(subset=["order_date"])
    # Видаляємо аномалії (total_amount <= 0 або quantity <= 0)
    orders = orders[(orders["total_amount"] > 0) & (orders["quantity"] > 0)]
    # Заповнюємо статус
    orders["status"] = orders["status"].fillna("pending")

    # --- PRODUCTS ---
    products = products.drop_duplicates()
    products["brand"] = products["brand"].fillna("Unknown")
    products["rating"] = products["rating"].fillna(products["rating"].mean())
    products["price"] = products["price"].fillna(products["price"].median())
    # Видаляємо аномалії цін (негативні або 0)
    products = products[products["price"] > 0]

    # --- REVIEWS ---
    reviews = reviews.drop_duplicates()
    reviews["review_date"] = pd.to_datetime(
        reviews["review_date"], format="mixed", errors="coerce"
    )
    reviews = reviews.dropna(subset=["review_date", "rating", "review_text"])
    # Фільтруємо рейтинг (зазвичай 1-5)
    reviews = reviews[(reviews["rating"] >= 1) & (reviews["rating"] <= 5)]

    return {
        "customers": customers,
        "orders": orders,
        "products": products,
        "reviews": reviews,
    }


# =========================================
# 2. АНАЛІЗ МЕТРИК
# =========================================

def calculate_kpi(data: dict) -> dict:
    """
    Розрахуйте ключові метрики бізнесу:

    KPI:
    - total_revenue: загальний дохід
    - total_orders: загальна кількість замовлень
    - avg_order_value: середній чек
    - avg_delivery_days: середній час доставки
    - repeat_rate: відсоток повторних клієнтів
    - top_city: місто з найбільшою кількістю замовлень
    - top_category: категорія з найбільшим доходом
    - revenue_by_month: дохід по місяцях

    Поверніть словник з KPI.
    """
    orders = data["orders"]
    customers = data["customers"]
    products = data["products"]

    # TODO: обчисліть метрики

    # Загальний дохід та кількість замовлень
    total_revenue = orders["total_amount"].sum()
    total_orders = len(orders)
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

    # Середній час доставки (дні)
    orders_delivered = orders[orders["delivery_date"].notna()].copy()
    orders_delivered["delivery_date"] = pd.to_datetime(
        orders_delivered["delivery_date"], format="mixed", errors="coerce"
    )
    orders_delivered = orders_delivered.dropna(subset=["delivery_date"])
    delivery_days = (orders_delivered["delivery_date"] - orders_delivered["order_date"]).dt.days
    # Фільтруємо аномалії (додатній час доставки, не більше 60 днів)
    delivery_days = delivery_days[(delivery_days > 0) & (delivery_days <= 60)]
    avg_delivery_days = float(delivery_days.mean()) if len(delivery_days) > 0 else None

    # Відсоток повторних клієнтів
    orders_per_customer = orders.groupby("customer_id").size()
    repeat_rate = float((orders_per_customer > 1).mean())

    # Місто з найбільшою кількістю замовлень
    orders_customers = pd.merge(orders, customers, on="customer_id", how="inner")
    top_city = orders_customers["city"].value_counts().idxmax()

    # Категорія з найбільшим доходом
    orders_products = pd.merge(orders, products, on="product_id", how="inner")
    top_category = (
        orders_products.groupby("category")["total_amount"].sum().idxmax()
    )

    # Дохід по місяцях
    revenue_by_month = (
        orders.set_index("order_date")
        .resample("ME")["total_amount"]
        .sum()
    )

    kpi = {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "avg_order_value": round(avg_order_value, 2),
        "avg_delivery_days": round(avg_delivery_days, 1) if avg_delivery_days else None,
        "repeat_rate": round(repeat_rate * 100, 1),
        "top_city": top_city,
        "top_category": top_category,
        "revenue_by_month": revenue_by_month,
    }
    return kpi


# =========================================
# 3. SQL ЗАПИТИ
# =========================================

def run_sql_queries(db_path: str = str(DB_PATH)) -> dict:
    """
    Напишіть та виконайте SQL запити до analytics.db:

    1. Топ-10 клієнтів за сумою замовлень
    2. Кількість замовлень по статусах
    3. Середній чек по місяцях за 2024 рік
    4. Категорії з найбільшою кількістю повернень
    5. Клієнти, які зробили >5 замовлень
    6. Топ-5 товарів за виручкою з віконною функцією RANK

    Поверніть словник {назва_запиту: DataFrame_результат}.
    """
    conn = sqlite3.connect(db_path)
    results = {}

    queries = {
        "top_customers": """
            SELECT c.customer_id, c.first_name || ' ' || c.last_name AS full_name,
                   ROUND(SUM(CAST(o.total_amount AS REAL)), 2) AS total_spent,
                   COUNT(o.order_id) AS order_count
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id
            ORDER BY total_spent DESC
            LIMIT 10
        """,
        "orders_by_status": """
            SELECT status, COUNT(*) AS order_count
            FROM orders
            GROUP BY status
            ORDER BY order_count DESC
        """,
        "monthly_avg_check_2024": """
            SELECT strftime('%m', order_date) AS month,
                   ROUND(AVG(CAST(total_amount AS REAL)), 2) AS avg_check,
                   COUNT(*) AS order_count
            FROM orders
            WHERE strftime('%Y', order_date) = '2024'
            GROUP BY month
            ORDER BY month
        """,
        "top_return_categories": """
            SELECT p.category, COUNT(r.return_id) AS return_count,
                   ROUND(SUM(CAST(r.refund_amount AS REAL)), 2) AS total_refunded
            FROM returns r
            JOIN orders o ON r.order_id = o.order_id
            JOIN products p ON o.product_id = p.product_id
            GROUP BY p.category
            ORDER BY return_count DESC
        """,
        "repeat_customers": """
            SELECT c.customer_id, c.first_name || ' ' || c.last_name AS full_name,
                   COUNT(o.order_id) AS order_count,
                   ROUND(SUM(CAST(o.total_amount AS REAL)), 2) AS total_spent
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id
            HAVING order_count > 5
            ORDER BY total_spent DESC
        """,
        "top_products_ranked": """
            SELECT product_name, category, total_revenue, rank
            FROM (
                SELECT p.product_name, p.category,
                       ROUND(SUM(CAST(o.total_amount AS REAL)), 2) AS total_revenue,
                       RANK() OVER (ORDER BY SUM(CAST(o.total_amount AS REAL)) DESC) AS rank
                FROM products p
                JOIN orders o ON p.product_id = o.product_id
                GROUP BY p.product_id
            )
            WHERE rank <= 5
            ORDER BY rank
        """,
    }

    for name, query in queries.items():
        try:
            results[name] = pd.read_sql_query(query, conn)
        except Exception as e:
            results[name] = pd.DataFrame({"error": [str(e)]})

    conn.close()
    return results


# =========================================
# 4. ВІЗУАЛІЗАЦІЇ
# =========================================

def create_visualizations(data: dict, kpi: dict) -> None:
    """
    Побудуйте графіки для презентації CEO:

    1. Дохід по місяцях (line chart) -> reports/revenue_trend.png
    2. Топ-10 категорій за доходом (bar chart) -> reports/top_categories.png
    3. Розподіл статусів замовлень (pie chart) -> reports/order_status_pie.png
    4. Теплова карта кореляції -> reports/final_heatmap.png
    """
    orders = data["orders"]
    products = data["products"]

    # 1. Дохід по місяцях
    fig, ax = plt.subplots(figsize=(12, 6))
    revenue_monthly = orders.set_index("order_date").resample("ME")["total_amount"].sum()
    ax.plot(revenue_monthly.index, revenue_monthly.values, marker="o", linewidth=2, color="green")
    ax.set_title("Дохід по місяцях", fontsize=14)
    ax.set_xlabel("Місяць")
    ax.set_ylabel("Дохід")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "revenue_trend.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("✓ revenue_trend.png збережено")

    # 2. Топ-10 категорій за доходом
    fig, ax = plt.subplots(figsize=(10, 6))
    orders_products = pd.merge(orders, products, on="product_id", how="inner")
    top_categories = (
        orders_products.groupby("category")["total_amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, 10))
    ax.bar(top_categories.index, top_categories.values, color=colors)
    ax.set_title("Топ-10 категорій за доходом", fontsize=14)
    ax.set_xlabel("Категорія")
    ax.set_ylabel("Дохід")
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "top_categories.png", dpi=100)
    plt.close()
    print("✓ top_categories.png збережено")

    # 3. Розподіл статусів замовлень (pie chart)
    fig, ax = plt.subplots(figsize=(8, 8))
    status_counts = orders["status"].value_counts()
    ax.pie(
        status_counts.values,
        labels=status_counts.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=plt.cm.Set3(np.linspace(0, 1, len(status_counts))),
    )
    ax.set_title("Розподіл статусів замовлень", fontsize=14)
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "order_status_pie.png", dpi=100)
    plt.close()
    print("✓ order_status_pie.png збережено")

    # 4. Теплова карта кореляції
    fig, ax = plt.subplots(figsize=(10, 8))
    numeric_cols = orders.select_dtypes(include=[np.number])
    corr = numeric_cols.corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
    ax.set_title("Кореляція числових змінних (orders)", fontsize=14)
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "final_heatmap.png", dpi=100)
    plt.close()
    print("✓ final_heatmap.png збережено")


# =========================================
# 5. БІЗНЕС-ВИСНОВКИ
# =========================================

def write_conclusions(kpi: dict) -> str:
    """
    На основі KPI напишіть бізнес-висновки для CEO.

    Формат:
    - 3-5 ключових висновків
    - 2-3 рекомендації
    - Потенційні ризики

    Поверніть текст висновків.
    """
    total_revenue = kpi["total_revenue"]
    avg_order_value = kpi["avg_order_value"]
    total_orders = kpi["total_orders"]
    repeat_rate = kpi["repeat_rate"]
    top_city = kpi["top_city"]
    top_category = kpi["top_category"]
    avg_delivery = kpi["avg_delivery_days"]

    conclusion = f"""
# Бізнес-висновки

## Ключові метрики
- Загальний дохід: {total_revenue:,.2f} грн
- Кількість замовлень: {total_orders:,}
- Середній чек: {avg_order_value:,.2f} грн
- Середній час доставки: {avg_delivery} днів
- Частка повторних клієнтів: {repeat_rate}%
- Найактивніше місто: {top_city}
- Найприбутковіша категорія: {top_category}

## Висновки
1. Середній чек складає {avg_order_value:,.2f} грн, що є важливим орієнтиром для маркетингових кампаній.
2. {repeat_rate}% клієнтів повертаються за повторними покупками — це показник лояльності клієнтів.
3. Найбільший дохід приносить категорія "{top_category}", що варто врахувати при формуванні асортименту.
4. Час доставки {avg_delivery} днів потребує оптимізації для підвищення задоволеності клієнтів.

## Рекомендації
1. Інвестувати в маркетинг у місті {top_city} — найбільш активному регіоні продажів.
2. Розширити асортимент у категорії "{top_category}" для збільшення доходу.
3. Впровадити програму лояльності для підвищення repeat rate з {repeat_rate}% до 40%+.

## Ризики
1. Високий відсоток скасувань або повернень може вказувати на проблеми з якістю.
2. Залежність від одного міста або категорії створює концентраційний ризик для бізнесу.
3. Якщо час доставки перевищує очікування клієнтів, це може вплинути на репутацію.
    """
    return conclusion.strip()


if __name__ == "__main__":
    print("=" * 60)
    print("📊 ФІНАЛЬНИЙ ПРОЄКТ: Junior Data Analyst")
    print("=" * 60)

    print("\n1. Очистка даних...")
    data = load_and_clean_data()

    print("\n2. Розрахунок KPI...")
    kpi = calculate_kpi(data)

    print("\n3. SQL запити...")
    sql_results = run_sql_queries()

    print("\n4. Візуалізації...")
    create_visualizations(data, kpi)

    print("\n5. Висновки...")
    conclusions = write_conclusions(kpi)
    print(conclusions)

    # Зберігаємо висновки
    with open(REPORTS_DIR / "conclusions.md", "w", encoding="utf-8") as f:
        f.write(conclusions)

    print("\n✅ Фінальний проєкт готовий!")
    print(f"📁 Звіт: {REPORTS_DIR}")
