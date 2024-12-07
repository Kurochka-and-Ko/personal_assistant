from managers.finance_manager import FinanceManager
from validators import *

def menu_finance():
    finance_manager = FinanceManager()
    while True:
        print("Меню финансов:")
        print("1. Добавить новую запись")
        print("2. Просмотреть все записи")
        print("3. Генерация отчёта")
        print("4. Экспортировать финансовые записи в CSV")
        print("5. Импортировать финансовые записи из CSV")
        print("0. Назад")
        choice = input("Выберите действие: ")

        if choice not in ['0', '1', '2', '3', '4', '5']:
            print("Некорректный выбор. Попробуйте снова.")
            continue

        if choice == '1':
            amount = input("Введите сумму (положительное для дохода, отрицательное для расхода): ")
            while not validate_number(amount):
                amount = input(
                    "Некорректная сумма. Введите число (положительное для дохода, отрицательное для расхода): ")
            amount = float(amount)

            category = input("Введите категорию (например, Еда, Транспорт): ")
            while not validate_non_empty_string(category):
                category = input("Категория не может быть пустой. Введите категорию (например, Еда, Транспорт): ")

            date = input("Введите дату (ДД-ММ-ГГГГ): ")
            while not validate_date(date):
                date = input("Некорректная дата. Введите дату в формате ДД-ММ-ГГГГ: ")

            description = input("Введите описание операции: ")
            while not validate_non_empty_string(description):
                description = input("Описание не может быть пустым. Введите описание операции: ")

            finance_manager.create_record(amount, category, date, description)
            print("Финансовая запись успешно добавлена!")

        elif choice == '2':
            filter_by_date = input(
                "Введите дату для фильтрации (ДД-ММ-ГГГГ) или оставьте пустым для просмотра всех записей: ")
            if filter_by_date and not validate_date(filter_by_date):
                print("Некорректная дата, фильтрация будет пропущена.")
                filter_by_date = None

            filter_by_category = input(
                "Введите категорию для фильтрации или оставьте пустым для просмотра всех записей: ")
            if filter_by_category and not validate_non_empty_string(filter_by_category):
                print("Категория не может быть пустой, фильтрация будет пропущена.")
                filter_by_category = None

            finance_manager.view_records(filter_by_date, filter_by_category)

        elif choice == '3':
            start_date = input("Введите начальную дату (ДД-ММ-ГГГГ): ")
            while not validate_date(start_date):
                start_date = input("Некорректная дата. Введите начальную дату в формате ДД-ММ-ГГГГ: ")

            end_date = input("Введите конечную дату (ДД-ММ-ГГГГ): ")
            while not validate_date(end_date):
                end_date = input("Некорректная дата. Введите конечную дату в формате ДД-ММ-ГГГГ: ")

            finance_manager.generate_report(start_date, end_date)

        elif choice == '4':
            filename = input("Введите имя файла для экспорта (по умолчанию finance_export.csv): ")
            filename = filename or 'finance_export.csv'
            while not validate_non_empty_string(filename):
                filename = input("Имя файла не может быть пустым. Введите имя файла для экспорта: ")
            finance_manager.export_records_to_csv(filename)
            print(f"Финансовые записи успешно экспортированы в {filename}!")

        elif choice == '5':
            filename = input("Введите имя файла для импорта (по умолчанию finance_export.csv): ")
            filename = filename or 'finance_export.csv'
            while not validate_non_empty_string(filename):
                filename = input("Имя файла не может быть пустым. Введите имя файла для импорта: ")
            finance_manager.import_records_from_csv(filename)
            print(f"Финансовые записи успешно импортированы из {filename}!")

        elif choice == '0':
            break

