from validators import *

def calculator1():
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
