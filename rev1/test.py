import json
data = 0

with open("test.json") as x:
    data = json.load(x)
    data['gector'] = data['gector'] + 1

with open("test.json", "w") as x:
    print(data)
    json.dump(data, x)
    # [] means you are accessing a value in a list/dictionary.

