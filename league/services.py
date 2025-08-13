import random


def generate_invite_code(length: int = 6) -> str:
    """Генерация уникального цифрового кода заданной длины"""
    assert length > 0, 'Длина кода должна быть минимум 1 символ'

    start = 10 ** (length - 1)
    end = (10 ** length) - 1

    code = str(random.randint(start, end))
    return code
