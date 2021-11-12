# Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты
# из байтовового в строковый тип на кириллице.


import subprocess
import chardet

YAND = ['ping', 'yandex.ru']
TUBE = ['ping', 'youtube.com']

YA_PING = subprocess.Popen(YAND, stdout=subprocess.PIPE)
TU_PING = subprocess.Popen(TUBE, stdout=subprocess.PIPE)

for line in YA_PING.stdout:
    result = chardet.detect(line)
    line = line.decode(result['encoding'])
    print(line)

for line in TU_PING.stdout:
    result = chardet.detect(line)
    line = line.decode(result['encoding'])
    print(line)
