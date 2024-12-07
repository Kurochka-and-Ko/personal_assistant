from managers.tasks_manager import TasksManager
from validators import *

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
