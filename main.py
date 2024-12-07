from menus.notes_menu import menu_notes
from menus.tasks_menu import menu_tasks
from menus.contacts_menu import menu_contacts
from menus.finance_menu import menu_finance
from menus.calculator2 import calculator1

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
            calculator1()
        elif choice == '6':
            print("Выход из программы. До свидания!")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")

if __name__ == '__main__':
    main_menu()