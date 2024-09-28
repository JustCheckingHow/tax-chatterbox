import requests

ADDR = "http://localhost:8000/api/upload"


def upload_test_file():
    with open("Umowa pożyczki - wzór.pdf", "rb") as f:
        response = requests.post(ADDR, files={"file": f})
        print("Response status code:", response.status_code)
        print(response.json())


if __name__ == "__main__":
    upload_test_file()
