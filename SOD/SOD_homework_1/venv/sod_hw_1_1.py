import requests
from pprint import pprint
import json
import codecs

main_link = 'http://dev.virtualearth.net/REST/v1/Locations/'
latitude = '47.64054'
longitude = '-122.12934'
output = 'json'
ApiKey = 'AklhwRIrv4nltkM43DRSmMqM_js0jnSSL2hVOFk2uP3uL1Rilsx-cGv9lyTlX_1E'
req = requests.get(f'{main_link}{latitude}{longitude}?o={output}&key={ApiKey}')

if req.ok:
    data = json.loads(req.text)
    pprint(data)

    with open('virtualearth.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    f.close()