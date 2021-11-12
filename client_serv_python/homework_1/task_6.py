# Создать текстовый файл test_file.txt, заполнить его тремя строками:
# «сетевое программирование», «сокет», «декоратор». Проверить кодировку файла по
# умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.


import locale
fed_enc = locale.getpreferredencoding()
print(f'Кодировка по-умолчанию: {fed_enc}')

WORDS = ['сетевое программирование', 'сокет', 'декоратор']
file = open('test_file.txt', 'w', encoding='utf-8')
for word in WORDS:
    file.write(word + '\n')
file.close()

# явное указание кодировки при работе с файлом
with open('test_file.txt', encoding='utf-8') as file:
    for line in file:
        print(line, end='')
