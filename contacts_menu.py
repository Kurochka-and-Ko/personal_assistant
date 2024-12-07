from managers.contacts_manager import ContactsManager
from validators import *

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
