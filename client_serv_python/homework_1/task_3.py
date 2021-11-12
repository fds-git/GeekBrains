# Определить, какие из слов «attribute», «класс», «функция», «type»
# невозможно записать в байтовом типе с помощью b.


WORDS = ['attribute', 'класс', 'функция', 'type']

for word in WORDS:
    try:
        expr = f"b'{word}'"
        exec(expr)
        print(f'Слово "{word}" можно записать в байтовом типе с помощью b')
    except SyntaxError:
        print(f'Слово "{word}" нельзя записать в байтовом типе с помощью b')
