import requests


def post_response(username: str, question: str, answer: str):
    url = "http://localhost:8080/question_answer"

    data = {"username": username, "question": question, "answer": answer}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("POST was successfull: ", response.json())
    else:
        print(f"POST failed. Status code: {response.status_code}")


# post_response("How are you?", "am fine")
def get_test():
    url = "http://localhost:8080/get_test"
    response = requests.get(url)
    if response.status_code == 200:
        print("Get was successfull: ", response.json())

    else:
        print("Get failed: ", response.status_code)

    return response.json()


# post_response(get_test()["question"], get_test()["answer"])
