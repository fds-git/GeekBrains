"""Модуль strings"""

# примеры строк
# переменные, объявленные на уровне модуля являются глобальными (константы
# в верхнем регистре)
FIRST_STR = 'Программирование'
print(FIRST_STR)
print(type(FIRST_STR))
SECOND_STR = 'Programování'
print(SECOND_STR)

# форматы записи юникод-символов
FIRST_SYMB = '\N{LATIN SMALL LETTER C WITH DOT ABOVE}'
print(FIRST_SYMB)

SECOND_SYMB = '\u010B'
print(SECOND_SYMB)

# строка, как последовательность юникод-символов
FIRST_WORD = 'Программа'
SECOND_WORD = '\u041f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0430'
print(type(SECOND_WORD))
print(SECOND_WORD)

print(FIRST_WORD == SECOND_WORD)

print(len(SECOND_WORD))

# функция ord позволяет получить числовое значение юникод-символа
print(ord('ã'))

# ункция chr позволяет получить символ по коду
print(chr(227))
