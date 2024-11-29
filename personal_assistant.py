import os
import csv
import datetime
import json
import re
from datetime import datetime

# Функция для проверки даты в формате ДД-ММ-ГГГГ
def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%d-%m-%Y')
        return True
    except ValueError:
        return False

# Проверка корректности телефона
def validate_phone_number(phone_str):
    pattern = r'^\+?\d{1,3}[-]?\(?\d{3}\)?[-]?\d{3}[-]?\d{4}$'
    return bool(re.match(pattern, phone_str))

# Проверка корректности email
def validate_email(email_str):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email_str))
# Функция для проверки числового ввода
def validate_number(number_str):
    try:
        float(number_str)
        return True
    except ValueError:
        return False
# Функция для проверки, что строка не пустая
def validate_non_empty_string(input_str):
    return bool(input_str.strip())
# Функция для проверки корректного ввода из предложенных вариантов
def validate_choice(valid_choices, choice):
    return choice in valid_choices

# Общие функции для работы с данными
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# ----- Модель заметки -----
class Note:
    def __init__(self, id, title, content, timestamp):
        self.id = id
        self.title = title
        self.content = content
        self.timestamp = timestamp

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'timestamp': self.timestamp
        }

# ----- Менеджер заметок -----
class NotesManager:
    def __init__(self):
        self.notes = []
        self.load_notes()

    def create_note(self, title, content):
        id = self.notes[-1].id + 1 if self.notes else 1
        timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        note = Note(id, title, content, timestamp)
        self.notes.append(note)
        self.save_notes()

    def edit_note(self, note_id, title=None, content=None):
        note = next((n for n in self.notes if n.id == note_id), None)
        if note:
            if title: note.title = title
            if content: note.content = content
            note.timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            self.save_notes()
        else:
            print("Заметка не найдена.")

    def delete_note(self, note_id):
        self.notes = [n for n in self.notes if n.id != note_id]
        self.save_notes()

    def view_notes(self):
        if not self.notes:
            print("Заметок нет.")
            return
        for note in self.notes:
            print(f"ID: {note.id}, Заголовок: {note.title}, Дата: {note.timestamp}")

    def view_note_details(self, note_id):
        note = next((n for n in self.notes if n.id == note_id), None)
        if note:
            print(f"Заголовок: {note.title}\nСодержание: {note.content}\nДата: {note.timestamp}")
        else:
            print("Заметка не найдена.")

    def export_notes_to_csv(self, filename="notes_export.csv"):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Title', 'Content', 'Timestamp'])
            for note in self.notes:
                writer.writerow([note.id, note.title, note.content, note.timestamp])
        print(f"Заметки экспортированы в файл {filename}")

    def import_notes_from_csv(self, filename="notes_export.csv"):
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.create_note(row['Title'], row['Content'])
        print("Заметки успешно импортированы.")

    def load_notes(self):
        data = load_data('notes.json')
        self.notes = [Note(**note) for note in data]

    def save_notes(self):
        data = [note.to_dict() for note in self.notes]
        save_data('notes.json', data)

# ----- Меню для заметок -----
def menu_notes():
    notes_manager = NotesManager()
    while True:
        print("Меню заметок:")
        print("1. Создать новую заметку")
        print("2. Просмотреть все заметки")
        print("3. Просмотреть подробности заметки")
        print("4. Редактировать заметку")
        print("5. Удалить заметку")
        print("6. Экспортировать заметки в CSV")
        print("7. Импортировать заметки из CSV")
        print("0. Назад")
        choice = input("Выберите действие: ")

        # Валидация выбора
        if choice not in ['0', '1', '2', '3', '4', '5', '6', '7']:
            print("Некорректный выбор. Попробуйте снова.")
            continue

        if choice == '1':  # Создание новой заметки
            title = input("Введите заголовок заметки: ")
            while not validate_non_empty_string(title):  # Валидация заголовка
                title = input("Заголовок не может быть пустым. Введите заголовок заметки: ")

            content = input("Введите содержание заметки: ")
            while not validate_non_empty_string(content):  # Валидация содержания
                content = input("Содержание не может быть пустым. Введите содержание заметки: ")

            notes_manager.create_note(title, content)
            print("Заметка успешно создана!")

        elif choice == '2':  # Просмотр всех заметок
            notes_manager.view_notes()

        elif choice == '3':  # Просмотр подробностей заметки
            note_id = input("Введите ID заметки: ")
            while not note_id.isdigit():  # Валидация ID
                note_id = input("Некорректный ID. Введите числовое значение: ")
            notes_manager.view_note_details(int(note_id))

        elif choice == '4':  # Редактирование заметки
            note_id = input("Введите ID заметки для редактирования: ")
            while not note_id.isdigit():  # Валидация ID
                note_id = input("Некорректный ID. Введите числовое значение: ")

            title = input("Введите новый заголовок (оставьте пустым для пропуска): ")
            content = input("Введите новое содержание (оставьте пустым для пропуска): ")

            # Если пользователь оставил пустые поля, пропускаем их при редактировании
            notes_manager.edit_note(int(note_id), title or None, content or None)
            print("Заметка успешно отредактирована!")

        elif choice == '5':  # Удаление заметки
            note_id = input("Введите ID заметки для удаления: ")
            while not note_id.isdigit():  # Валидация ID
                note_id = input("Некорректный ID. Введите числовое значение: ")
            notes_manager.delete_note(int(note_id))
            print("Заметка успешно удалена!")

        elif choice == '6':  # Экспорт заметок в CSV
            filename = input("Введите имя файла для экспорта (по умолчанию notes_export.csv): ")
            filename = filename or 'notes_export.csv'  # Если имя пустое, используется default
            while not validate_non_empty_string(filename):  # Валидация имени файла
                filename = input("Имя файла не может быть пустым. Введите имя файла для экспорта: ")
            notes_manager.export_notes_to_csv(filename)
            print(f"Заметки успешно экспортированы в {filename}!")

        elif choice == '7':  # Импорт заметок из CSV
            filename = input("Введите имя файла для импорта (по умолчанию notes_export.csv): ")
            filename = filename or 'notes_export.csv'  # Если имя пустое, используется default
            while not validate_non_empty_string(filename):  # Валидация имени файла
                filename = input("Имя файла не может быть пустым. Введите имя файла для импорта: ")
            notes_manager.import_notes_from_csv(filename)
            print(f"Заметки успешно импортированы из {filename}!")

        elif choice == '0':  # Назад
            break


# ----- Модель задачи -----
class Task:
    def __init__(self, id, title, description, done, priority, due_date):
        self.id = id
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'done': self.done,
            'priority': self.priority,
            'due_date': self.due_date
        }

# ----- Менеджер задач -----
class TasksManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def create_task(self, title, description, priority, due_date):
        id = self.tasks[-1].id + 1 if self.tasks else 1
        task = Task(id, title, description, done=False, priority=priority, due_date=due_date)
        self.tasks.append(task)
        self.save_tasks()

    def edit_task(self, task_id, title=None, description=None, priority=None, due_date=None):
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task:
            if title: task.title = title
            if description: task.description = description
            if priority: task.priority = priority
            if due_date: task.due_date = due_date
            self.save_tasks()
        else:
            print("Задача не найдена.")

    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t.id != task_id]
        self.save_tasks()

    def mark_task_as_done(self, task_id):
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task:
            task.done = True
            self.save_tasks()
        else:
            print("Задача не найдена.")

    def view_tasks(self):
        if not self.tasks:
            print("Задач нет.")
            return
        for task in self.tasks:
            status = "Выполнена" if task.done else "Не выполнена"
            print(f"ID: {task.id}, Заголовок: {task.title}, Приоритет: {task.priority}, Срок: {task.due_date}, Статус: {status}")

    def export_tasks_to_csv(self, filename="tasks_export.csv"):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Title', 'Description', 'Done', 'Priority', 'Due Date'])
            for task in self.tasks:
                writer.writerow([task.id, task.title, task.description, task.done, task.priority, task.due_date])
        print(f"Задачи экспортированы в файл {filename}")

    def import_tasks_from_csv(self, filename="tasks_export.csv"):
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.create_task(row['Title'], row['Description'], row['Priority'], row['Due Date'])
        print("Задачи успешно импортированы.")

    def load_tasks(self):
        data = load_data('tasks.json')
        self.tasks = [Task(**task) for task in data]

    def save_tasks(self):
        data = [task.to_dict() for task in self.tasks]
        save_data('tasks.json', data)

# ----- Меню для задач -----
def menu_tasks():
    tasks = TasksManager()  # Пример: TasksManager должен быть реализован в твоем коде
    while True:
        print("Меню задач:")
        print("1. Добавить новую задачу.")
        print("2. Просмотреть задачи.")
        print("3. Отметить задачу как выполненную.")
        print("4. Редактировать задачу.")
        print("5. Удалить задачу.")
        print("6. Экспорт задач в CSV.")
        print("7. Импорт задач из CSV.")
        print("8. Назад.")
        choice = input("Выберите действие: ")

        if not validate_choice([str(i) for i in range(1, 9)], choice):
            print("Некорректный ввод, попробуйте снова.")
            continue

        if choice == '1':  # Добавление новой задачи
            title = input("Введите название задачи: ")
            while not validate_non_empty_string(title):
                title = input("Название не может быть пустым. Введите название задачи: ")

            description = input("Введите описание задачи: ")
            while not validate_non_empty_string(description):
                description = input("Описание не может быть пустым. Введите описание задачи: ")

            priority = input("Выберите приоритет (Высокий/Средний/Низкий): ")
            while priority not in ["Высокий", "Средний", "Низкий"]:
                priority = input("Некорректный приоритет. Выберите приоритет (Высокий/Средний/Низкий): ")

            due_date = input("Введите срок выполнения задачи (ДД-ММ-ГГГГ): ")
            while not validate_date(due_date):
                due_date = input("Некорректная дата. Введите срок выполнения задачи (ДД-ММ-ГГГГ): ")

            tasks.add_task(title, description, priority, due_date)
            print("Задача успешно добавлена!")

        elif choice == '2':  # Просмотр задач
            tasks.view_tasks()

        elif choice == '8':  # Назад
            break

# ----- Модель контакта -----
class Contact:
    def __init__(self, id, name, phone, email):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email
        }

# ----- Менеджер контактов -----
class ContactsManager:
    def __init__(self):
        self.contacts = []
        self.load_contacts()

    def create_contact(self, name, phone, email):
        id = self.contacts[-1].id + 1 if self.contacts else 1
        contact = Contact(id, name, phone, email)
        self.contacts.append(contact)
        self.save_contacts()

    def edit_contact(self, contact_id, name=None, phone=None, email=None):
        contact = next((c for c in self.contacts if c.id == contact_id), None)
        if contact:
            if name: contact.name = name
            if phone: contact.phone = phone
            if email: contact.email = email
            self.save_contacts()
        else:
            print("Контакт не найден.")

    def delete_contact(self, contact_id):
        self.contacts = [c for c in self.contacts if c.id != contact_id]
        self.save_contacts()

    def search_contact(self, search_term):
        found_contacts = [c for c in self.contacts if search_term.lower() in c.name.lower() or search_term in c.phone]
        if not found_contacts:
            print("Контакты не найдены.")
        else:
            for contact in found_contacts:
                print(f"ID: {contact.id}, Имя: {contact.name}, Телефон: {contact.phone}, Email: {contact.email}")

    def view_contacts(self):
        if not self.contacts:
            print("Контакты не найдены.")
            return
        for contact in self.contacts:
            print(f"ID: {contact.id}, Имя: {contact.name}, Телефон: {contact.phone}, Email: {contact.email}")

    def export_contacts_to_csv(self, filename="contacts_export.csv"):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Name', 'Phone', 'Email'])
            for contact in self.contacts:
                writer.writerow([contact.id, contact.name, contact.phone, contact.email])
        print(f"Контакты экспортированы в файл {filename}")

    def import_contacts_from_csv(self, filename="contacts_export.csv"):
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.create_contact(row['Name'], row['Phone'], row['Email'])
        print("Контакты успешно импортированы.")

    def load_contacts(self):
        data = load_data('contacts.json')
        self.contacts = [Contact(**contact) for contact in data]

    def save_contacts(self):
        data = [contact.to_dict() for contact in self.contacts]
        save_data('contacts.json', data)

# ----- Меню для контактов -----
def menu_contacts():
    contacts_manager = ContactsManager()
    while True:
        print("Меню контактов:")
        print("1. Добавить новый контакт")
        print("2. Просмотреть все контакты")
        print("3. Поиск контакта")
        print("4. Редактировать контакт")
        print("5. Удалить контакт")
        print("6. Экспортировать контакты в CSV")
        print("7. Импортировать контакты из CSV")
        print("0. Назад")
        choice = input("Выберите действие: ")

        # Валидация выбора
        if choice not in ['0', '1', '2', '3', '4', '5', '6', '7']:
            print("Некорректный выбор. Попробуйте снова.")
            continue

        if choice == '1':
            name = input("Введите имя контакта: ")
            while not validate_non_empty_string(name):
                name = input("Имя не может быть пустым. Введите имя контакта: ")

            phone = input("Введите номер телефона контакта: ")
            while not validate_phone_number(phone):
                phone = input("Неверный формат номера. Введите номер телефона (формат: +X-XXX-XXX-XXXX): ")

            email = input("Введите email контакта: ")
            while not validate_email(email):
                email = input("Неверный формат email. Введите корректный email: ")

            contacts_manager.create_contact(name, phone, email)
            print("Контакт успешно добавлен!")

        elif choice == '2':
            contacts_manager.view_contacts()

        elif choice == '3':
            search_term = input("Введите имя или номер телефона для поиска: ")
            contacts_manager.search_contact(search_term)

        elif choice == '4':
            contact_id = input("Введите ID контакта для редактирования: ")
            while not contact_id.isdigit():
                contact_id = input("Некорректный ID. Введите числовое значение: ")

            name = input("Введите новое имя (оставьте пустым для пропуска): ")
            phone = input("Введите новый номер телефона (оставьте пустым для пропуска): ")
            email = input("Введите новый email (оставьте пустым для пропуска): ")

            contacts_manager.edit_contact(int(contact_id), name or None, phone or None, email or None)
            print("Контакт успешно отредактирован!")

        elif choice == '5':
            contact_id = input("Введите ID контакта для удаления: ")
            while not contact_id.isdigit():
                contact_id = input("Некорректный ID. Введите числовое значение: ")
            contacts_manager.delete_contact(int(contact_id))
            print("Контакт успешно удален!")

        elif choice == '6':
            filename = input("Введите имя файла для экспорта (по умолчанию contacts_export.csv): ")
            filename = filename or 'contacts_export.csv'
            while not validate_non_empty_string(filename):
                filename = input("Имя файла не может быть пустым. Введите имя файла для экспорта: ")
            contacts_manager.export_contacts_to_csv(filename)
            print(f"Контакты успешно экспортированы в {filename}!")

        elif choice == '7':
            filename = input("Введите имя файла для импорта (по умолчанию contacts_export.csv): ")
            filename = filename or 'contacts_export.csv'
            while not validate_non_empty_string(filename):
                filename = input("Имя файла не может быть пустым. Введите имя файла для импорта: ")
            contacts_manager.import_contacts_from_csv(filename)
            print(f"Контакты успешно импортированы из {filename}!")

        elif choice == '0':
            break

# ----- Модель финансовой записи -----
class FinanceRecord:
    def __init__(self, id, amount, category, date, description):
        self.id = id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'date': self.date,
            'description': self.description
        }

# ----- Менеджер финансовых записей -----
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

# ----- Меню для финансов -----
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


# ----- Калькулятор -----
def calculator():
    while True:
        print("Калькулятор:")
        print("1. Сложение")
        print("2. Вычитание")
        print("3. Умножение")
        print("4. Деление")
        print("0. Выход")
        choice = input("Выберите операцию: ")

        if choice not in ['0', '1', '2', '3', '4']:
            print("Некорректный выбор. Попробуйте снова.")
            continue

        if choice == '0':
            print("Выход из калькулятора.")
            break

        num1 = input("Введите первое число: ")
        while not validate_number(num1):
            num1 = input("Ошибка: Пожалуйста, введите корректное число. Попробуйте снова: ")
        num1 = float(num1)

        num2 = input("Введите второе число: ")
        while not validate_number(num2):
            num2 = input("Ошибка: Пожалуйста, введите корректное число. Попробуйте снова: ")
        num2 = float(num2)

        if choice == '1':
            result = num1 + num2
            print(f"Результат: {result}")
        elif choice == '2':
            result = num1 - num2
            print(f"Результат: {result}")
        elif choice == '3':
            result = num1 * num2
            print(f"Результат: {result}")
        elif choice == '4':
            if num2 == 0:
                print("Ошибка: Деление на ноль!")
            else:
                result = num1 / num2
                print(f"Результат: {result}")

# ----- Главное меню -----
def main_menu():
    while True:
        print("Добро пожаловать в Персональный помощник!")
        print("Выберите действие:")
        print("1. Управление заметками")
        print("2. Управление задачами")
        print("3. Управление контактами")
        print("4. Управление финансовыми записями")
        print("5. Калькулятор")
        print("6. Выход")
        choice = input("Введите номер действия: ")

        if choice == '1':
            menu_notes()
        elif choice == '2':
            menu_tasks()
        elif choice == '3':
            menu_contacts()
        elif choice == '4':
            menu_finance()
        elif choice == '5':
            calculator()
        elif choice == '6':
            print("Выход из программы. До свидания!")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")

if __name__ == '__main__':
    main_menu()