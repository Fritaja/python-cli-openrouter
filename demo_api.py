import json
import urllib.request
import urllib.error

url = "https://jsonplaceholder.typicode.com/users/1"

try:
    with urllib.request.urlopen(url, timeout=10) as response:
        print("HTTP Status:", response.status)
        data = response.read().decode("utf-8")

    user = json.loads(data)

    print("Name:", user["name"])
    print("Email:", user["email"])
    print("City:", user["address"]["city"])

except urllib.error.HTTPError as error:
    print("HTTP Error:", error.code)

except urllib.error.URLError as error:
    print("Connection Error:", error.reason)
