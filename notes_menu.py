from managers.notes_manager import NotesManager
from validators import validate_non_empty_string


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