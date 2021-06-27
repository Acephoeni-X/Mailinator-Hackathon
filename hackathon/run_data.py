import json

with open ('data.json', 'r+') as f:
    i = json.loads(f.read())
    print(i[0]['time'])