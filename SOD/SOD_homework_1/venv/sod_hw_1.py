import requests
from pprint import pprint
import json

req = requests.get('https://api.github.com/users/Dmitry0303/repos')

if req.ok:
    data = json.loads(req.text)
    for d in data:
        print(d['name'])

    with open('git_rep.json','w') as file:
        data = json.loads(req.text)
        for d in data:
            file.write(d['name'])

    file.close()








