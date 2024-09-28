import base64
import io
import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from pdf2image import convert_from_path
from PIL import Image

load_dotenv()


OUTPUT_FORMAT_SYS = """
Podaj dane w poniższym formacie:
{
    "imie_nazwisko_kupujacy_lub_pozyczkobiorca": "Twoja odpowiedz",
    "imie_nazwisko_sprzedawca_lub_pozyczkobiorca": "Twoja odpowiedz",
    "PESEL_kupujacy_lub_pozyczkobiorca": "Twoja odpowiedz",
    "PESEL_sprzedawca_lub_pozyczkodawca": "Twoja odpowiedz",
    "zamieszkanie_kupujacy_lub_pozyczkobiorca": "Twoja odpowiedz",
    "zamieszkanie_sprzedawca_lub_pozyczkodawca": "Twoja odpowiedz",
    "kwota_sprzedazy": "Twoja odpowiedz",
    "miejsce_zawracia_umowy": "Twoja odpowiedz",
    "data_zawarcia_umowy": "Twoja odpowiedź"
}
Nie odbiegaj od powyższego formatu. W razie braku informacji, pozostaw pole puste
"""


def submit_pdf(image_path, img_size: int = 900):
    openai_api_key = os.getenv("RUNPOD_API_KEY")
    openai_api_base = "https://ep2z4vudsnqp7g-8000.proxy.runpod.net/v1"
    # min_pixels=32 * 28 * 28, max_pixels=1920 * 28 * 28
    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )
    with open(image_path, "rb") as f:
        image = Image.open(f)
        resized_image = image.resize((img_size, img_size))
        buffered = io.BytesIO()
        resized_image.save(buffered, format="JPEG")
        encoded_image = base64.b64encode(buffered.getvalue())
    encoded_image_text = encoded_image.decode("utf-8")
    base64_qwen = f"data:image;base64,{encoded_image_text}"
    chat_response = client.chat.completions.create(
        model="Qwen/Qwen2-VL-7B-Instruct",
        messages=[
            {
                "role": "system",
                "content": "Jesteś OCRem do czytania polskiego tekstu z obrazków. Specjalizujesz się w czytaniu pisma "
                "odręcznego, nawet jeżeli jest bardzo trudne do odczytania.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": base64_qwen},
                        "min_pixels": 32 * 28 * 28,
                        "max_pixels": 1920 * 28 * 28,
                    },
                    {
                        "type": "text",
                        "text": "Wciągnij z tekstu dane dotyczące umowy. " + OUTPUT_FORMAT_SYS,
                    },
                ],
            },
        ],
    )
    # print("Chat response:", chat_response)
    resp = chat_response.choices[0].message.content
    try:
        resp_json = json.loads(resp)
    except json.JSONDecodeError:
        print(resp_json)

    return resp


def extract_pdf_info(path: str):
    pages = convert_from_path(path, 500)
    for count, page in enumerate(pages):
        page.save(f"umow_{count}.jpg", "JPEG")


if __name__ == "__main__":
    # extract_pdf_info("/Users/jm/repos/tax-chatterbox/Umowa pożyczki - wzór.pdf")
    print(submit_pdf("/Users/jm/repos/tax-chatterbox/umow_0.jpg"))
