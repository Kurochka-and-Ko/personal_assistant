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
