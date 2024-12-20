import re


def validate_password(password):
    """Проверяет, что пароль соответствует требованиям (минимум 5 латинских букв и 2 цифры)."""
    if len(password) < 8:
        return False

    letters = re.findall(r"[a-zA-Z]", password)
    digits = re.findall(r"[0-9]", password)

    return len(letters) >= 5 and len(digits) >= 3
