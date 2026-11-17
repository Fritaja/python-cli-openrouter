
import json
import urllib.request
import urllib.error

url = "https://jsonplaceholder.typicode.com/posts"

data = {
    "title": "My first API request",
    "body": "Learning Python HTTP POST",
    "userId": 1
}

json_data = json.dumps(data).encode("utf-8")

request = urllib.request.Request(
    url,
    data=json_data,
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    with urllib.request.urlopen(request, timeout=10) as response:
        print("HTTP Status:", response.status)
        result = response.read().decode("utf-8")

    response_data = json.loads(result)

    print("Created post ID:", response_data["id"])
    print("Title:", response_data["title"])
    print("Body:", response_data["body"])

except urllib.error.HTTPError as error:
    print("HTTP Error:", error.code)

except urllib.error.URLError as error:
    print("Connection Error:", error.reason)

