import requests

ADDR = "http://localhost:8000/api/closestUrzad"


def get_closests():
    response = requests.post(
        ADDR, data={"location": "ul. Wrocławska 53, 30-011 Kraków"}
    )
    print("Response status code:", response.status_code)
    print(response.json())


if __name__ == "__main__":
    get_closests()
