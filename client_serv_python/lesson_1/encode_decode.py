"""Модуль encode_decode"""

# простое кодирование - encode
ENC_STR = 'Кодировка'
ENC_STR_BYTES = ENC_STR.encode('utf-8')
print(ENC_STR_BYTES)

# простое декодирование - decode
DEC_STR_BYTES = b'\xd0\x9a\xd0\xbe\xd0\xb4\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xba\xd0\xb0'
DEC_STR = DEC_STR_BYTES.decode('utf-8')
print(DEC_STR)

# метод encode для класса str (кодировка указана как ключевой аргумент)
ENC_STR = 'Программа'
ENC_STR_BYTES = str.encode(ENC_STR, encoding='utf-8')
print(ENC_STR_BYTES)

# метод decode для класса bytes (кодировка указана как ключевой аргумент)
BYTES_OBJ = b'\xd0\x9f\xd1\x80\xd0\xbe\xd0\xb3\xd1\x80\xd0\xb0\xd0\xbc\xd0\xbc\xd0\xb0'
BYTES_DEC = bytes.decode(BYTES_OBJ, encoding='utf-8')
print(BYTES_DEC)
