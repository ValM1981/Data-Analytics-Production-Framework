#!/usr/bin/env python3
"""
Data Analytics Training Project — Єдина точка входу.

Використання:
    python main.py generate          # Генерація даних
    python main.py dashboard [name]  # Запуск дашборду
    python main.py grade             # Перевірка завдань
    python main.py run <script>      # Запуск скрипта
    python main.py clean             # Очищення даних
    python main.py test              # Запуск тестів
    python main.py                   # Інтерактивне меню
"""

import sys
import os
import logging
from pathlib import Path

# Додаємо корінь проєкту в sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.config_loader import load_config
from src.utils.logger import setup_logging

logger = logging.getLogger("main")


def has_data(config: dict) -> bool:
    """Перевіряє наявність ключових файлів даних."""
    raw_dir = Path(config["paths"]["raw_data"])
    required = [
        "customers.csv",
        "orders.csv",
        "products.csv",
        "payments.csv",
        "reviews.csv",
    ]
    return all((raw_dir / f).exists() for f in required)


def cmd_generate(config: dict) -> None:
    """Генерація всіх даних."""
    logger.info("🔄 Генерація даних...")
    from src.data_generator.generate_all import generate_all
    generate_all(config)
    logger.info("✅ Генерація завершена")


def cmd_dashboard(config: dict, name: str | None = None) -> None:
    """Запуск дашбордів."""
    logger.info(f"📊 Запуск дашборду: {name or 'всі'}")
    from src.visualization.dashboard_runner import run_dashboard
    run_dashboard(config, name)


def cmd_grade(config: dict) -> None:
    """Запуск перевірки завдань."""
    logger.info("📝 Запуск перевірки...")
    from grader import run_grader
    run_grader(config)
    logger.info("✅ Перевірка завершена")


def cmd_run(config: dict, script_name: str) -> None:
    """Запуск конкретного скрипта з scripts/."""
    scripts_dir = Path(config["paths"]["scripts"])
    script_path = scripts_dir / script_name

    if not script_path.suffix:
        script_path = script_path.with_suffix(".py")

    if not script_path.exists():
        logger.error(f"❌ Скрипт не знайдено: {script_path}")
        sys.exit(1)

    logger.info(f"▶️ Запуск {script_path.name}...")

    # Виконуємо файл у поточному контексті
    with open(script_path, encoding="utf-8") as f:
        code = compile(f.read(), script_path.name, "exec")
    exec(code, {"__name__": "__main__", "__file__": str(script_path)})

    logger.info(f"✅ {script_path.name} виконано")


def cmd_clean(config: dict) -> None:
    """Очищення даних."""
    logger.info("🧹 Запуск очищення даних...")
    from src.cleaning.clean_data import run_cleaning
    run_cleaning(config)
    logger.info("✅ Очищення завершене")


def cmd_test(config: dict) -> None:
    """Запуск тестів."""
    logger.info("🧪 Запуск тестів...")
    import pytest
    tests_dir = Path(config["paths"]["tests"])
    exit_code = pytest.main([str(tests_dir), "-v"])
    if exit_code == 0:
        logger.info("✅ Всі тести пройдено")
    else:
        logger.error(f"❌ Тести не пройдено (код: {exit_code})")


def show_interactive_menu(config: dict) -> None:
    """Інтерактивне меню."""
    menus = [
        ("1", "🔄 Згенерувати дані", "generate"),
        ("2", "📊 Запустити всі дашборди", "dashboard_all"),
        ("3", "📊 Sales Dashboard", "dashboard_sales"),
        ("4", "📊 Customer Dashboard", "dashboard_customer"),
        ("5", "📊 Marketing Dashboard", "dashboard_marketing"),
        ("6", "📊 Product Dashboard", "dashboard_product"),
        ("7", "📝 Перевірити завдання", "grade"),
        ("8", "▶️ Запустити NumPy задачі", "run_numpy"),
        ("9", "▶️ Запустити Pandas задачі", "run_pandas"),
        ("10", "▶️ Запустити Visualization задачі", "run_viz"),
        ("11", "▶️ Запустити фінальний проєкт", "run_final"),
        ("12", "🧹 Очистити дані", "clean"),
        ("13", "🧪 Запустити тести", "test"),
        ("0", "❌ Вийти", "exit"),
    ]

    print("\n" + "=" * 60)
    print("  📊 DATA ANALYTICS TRAINING PROJECT")
    print("=" * 60)
    for key, label, _ in menus:
        print(f"  {key}. {label}")
    print("=" * 60)

    choice = input("\n👉 Оберіть опцію: ").strip()

    action_map = {
        "1": lambda: cmd_generate(config),
        "2": lambda: cmd_dashboard(config),
        "3": lambda: cmd_dashboard(config, "sales"),
        "4": lambda: cmd_dashboard(config, "customer"),
        "5": lambda: cmd_dashboard(config, "marketing"),
        "6": lambda: cmd_dashboard(config, "product"),
        "7": lambda: cmd_grade(config),
        "8": lambda: cmd_run(config, "01_numpy_tasks"),
        "9": lambda: cmd_run(config, "02_pandas_tasks"),
        "10": lambda: cmd_run(config, "03_visualization_tasks"),
        "11": lambda: cmd_run(config, "final_project"),
        "12": lambda: cmd_clean(config),
        "13": lambda: cmd_test(config),
        "0": lambda: sys.exit(0),
    }

    action = action_map.get(choice)
    if action:
        action()
    else:
        logger.warning("⚠️ Невірний вибір")


def main():
    config = load_config(PROJECT_ROOT / "config.yaml")
    setup_logging(config)

    args = sys.argv[1:]

    if not args:
        # Авто-генерація, якщо даних нема
        if not has_data(config):
            logger.info("📦 Дані не знайдено. Автоматична генерація...")
            cmd_generate(config)
        show_interactive_menu(config)
        return

    command = args[0]
    arg = args[1] if len(args) > 1 else None

    commands = {
        "generate": lambda: cmd_generate(config),
        "dashboard": lambda: cmd_dashboard(config, arg),
        "grade": lambda: cmd_grade(config),
        "run": lambda: cmd_run(config, arg) if arg else (
            logger.error("❌ Вкажіть назву скрипта: python main.py run <script_name>"),
            sys.exit(1)
        ),
        "clean": lambda: cmd_clean(config),
        "test": lambda: cmd_test(config),
        "menu": lambda: show_interactive_menu(config),
    }

    cmd = commands.get(command)
    if cmd:
        cmd()
    else:
        logger.error(f"❌ Невідома команда: {command}")
        print("Доступні команди: generate, dashboard, grade, run, clean, test, menu")
        sys.exit(1)


if __name__ == "__main__":
    main()
