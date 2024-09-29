import requests

ADDR = "http://localhost:8001/api/validate_infer"


def get_data_from_postal():
    response = requests.post(ADDR, data={"KodPocztowy": "30-343"})
    print("Response status code:", response.status_code)
    print(response.json())


def get_data_from_pesel():
    response = requests.post(ADDR, data={"Pesel": "96031305018"})
    print("Response status code:", response.status_code)
    print(response.json())

def get_data_from_pesel():
    response = requests.post(ADDR, data={"Miejscowosc": "Kraków"})
    print("Response status code:", response.status_code)
    print(response.json())

if __name__ == "__main__":
    # get_data_from_postal()
    get_data_from_pesel()