import csv
from models.finance import FinanceRecord
from data_handler import load_data, save_data


class FinanceManager:
    def __init__(self):
        self.records = []
        self.load_records()

    def create_record(self, amount, category, date, description):
        id = self.records[-1].id + 1 if self.records else 1
        record = FinanceRecord(id, amount, category, date, description)
        self.records.append(record)
        self.save_records()

    def view_records(self, filter_by_date=None, filter_by_category=None):
        filtered_records = self.records
        if filter_by_date:
            filtered_records = [r for r in filtered_records if r.date == filter_by_date]
        if filter_by_category:
            filtered_records = [r for r in filtered_records if r.category.lower() == filter_by_category.lower()]

        if not filtered_records:
            print("Нет записей, соответствующих фильтру.")
        else:
            for record in filtered_records:
                print(f"ID: {record.id}, Сумма: {record.amount}, Категория: {record.category}, Дата: {record.date}, Описание: {record.description}")

    def generate_report(self, start_date, end_date):
        total_income = 0
        total_expenses = 0
        filtered_records = [r for r in self.records if start_date <= r.date <= end_date]
        for record in filtered_records:
            if record.amount > 0:
                total_income += record.amount
            else:
                total_expenses += record.amount
        balance = total_income + total_expenses  # так как расходы отрицательны

        report_filename = f"report_{start_date}_{end_date}.csv"
        with open(report_filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Amount', 'Category', 'Date', 'Description'])
            for record in filtered_records:
                writer.writerow([record.id, record.amount, record.category, record.date, record.description])

        print(f"Финансовый отчет за период с {start_date} по {end_date}:")
        print(f"Общий доход: {total_income} руб.")
        print(f"Общие расходы: {total_expenses} руб.")
        print(f"Баланс: {balance} руб.")
        print(f"Подробная информация сохранена в файл {report_filename}")

    def export_records_to_csv(self, filename="finance_export.csv"):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Amount', 'Category', 'Date', 'Description'])
            for record in self.records:
                writer.writerow([record.id, record.amount, record.category, record.date, record.description])
        print(f"Финансовые записи экспортированы в файл {filename}")

    def import_records_from_csv(self, filename="finance_export.csv"):
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.create_record(float(row['Amount']), row['Category'], row['Date'], row['Description'])
        print("Финансовые записи успешно импортированы.")

    def load_records(self):
        data = load_data('finance.json')
        self.records = [FinanceRecord(**record) for record in data]

    def save_records(self):
        data = [record.to_dict() for record in self.records]
        save_data('finance.json', data)
