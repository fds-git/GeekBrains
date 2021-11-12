# Преобразовать слова «разработка», «администрирование», «protocol», «standard»
# из строкового представления в байтовое и выполнить обратное преобразование
# (используя методы encode и decode).


WORDS = ['разработка', 'администрирование', 'protocol', 'standard']
WORDS_BYTE = []
WORDS_LETTER = []
for word in WORDS:
    word_byte = word.encode('utf-8')
    WORDS_BYTE.append(word_byte)
    WORDS_LETTER.append(word_byte.decode('utf-8'))

print(WORDS_BYTE)
print(WORDS_LETTER)
