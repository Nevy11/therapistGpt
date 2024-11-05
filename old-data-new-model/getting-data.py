import requests

def get_question():
    url = "http://localhost:4200"

    response=requests.get(url)
    if response.status_code == 200:
        print("Response Content: ", response.json())
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

get_question()
