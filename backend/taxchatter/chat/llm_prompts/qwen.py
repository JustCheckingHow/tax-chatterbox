import base64
import io
import json
import os
import tempfile

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
Nie odbiegaj od powyższego formatu. Gdy danej informacji nie ma w obrazie, pozostaw pole puste.
Nie próbuj wypełniać pola, jeżeli nie masz odpowiedniej wystarczająco informacji.
"""


def get_qwen_deployment():
    openai_api_key = os.getenv("RUNPOD_API_KEY")
    openai_api_base = "https://ep2z4vudsnqp7g-8000.proxy.runpod.net/v1"
    # min_pixels=32 * 28 * 28, max_pixels=1920 * 28 * 28
    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )
    return client


def get_extract_messages(base64_qwen: str):
    return [
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
    ]


def get_ocr_chat_messages(base64_qwen: str):
    return [
        {
            "role": "system",
            "content": "Jesteś wyśmienitym OCRem do czytania polskiego tekstu z obrazków. "
            "Specjalizujesz się w odczytywaniu tekstów umów, nawet jeżeli jest bardzo trudne do odczytania. "
            "Podaj użytkownikowi dokładnie treść pisma. "
            "Nie dodawaj nic od siebie.",
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
                    "text": "Podaj treść pisma na obrazku.",
                },
            ],
        },
    ]


def preproc_img(image_path, img_size: int = 900):
    with open(image_path, "rb") as f:
        image = Image.open(f)
        resized_image = image.resize((img_size, img_size))
        buffered = io.BytesIO()
        resized_image.save(buffered, format="JPEG")
        encoded_image = base64.b64encode(buffered.getvalue())
    encoded_image_text = encoded_image.decode("utf-8")
    return f"data:image;base64,{encoded_image_text}"


def ocr_pdf(pdf_path: str, img_size: int = 900, pdf_dpi: int = 500):
    pages = convert_from_path(pdf_path, pdf_dpi)
    ocr_pages = []
    import time

    for _, page in enumerate(pages):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            page.save(temp_file, "JPEG")
            response = submit_image(temp_file.name, img_msg=get_ocr_chat_messages, img_size=img_size)
            time.sleep(2)
            ocr_pages.append(response)
    return ocr_pages


def extract_pdf(pdf_path: str, img_size: int = 900, pdf_dpi: int = 500):
    pages = convert_from_path(pdf_path, pdf_dpi)
    ocr_pages = []
    for _, page in enumerate(pages):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            page.save(temp_file, "JPEG")
            response = submit_image(temp_file.name, img_msg=get_extract_messages, img_size=img_size)
            ocr_pages.append(response)
    return ocr_pages


def submit_image(
    image_path,
    img_msg: callable,
    img_size: int = 900,
):
    client = get_qwen_deployment()
    base64_qwen = preproc_img(image_path, img_size)

    chat_response = client.chat.completions.create(
        model="Qwen/Qwen2-VL-7B-Instruct",
        messages=img_msg(base64_qwen),
        temperature=0.0,
    )
    resp = chat_response.choices[0].message.content
    if img_msg == get_ocr_chat_messages:
        return resp
    return json.loads(resp)


if __name__ == "__main__":
    print(
        ocr_pdf(
            "/Users/jm/repos/tax-chatterbox/Umowa pożyczki - wzór.pdf",
            img_size=900,
            pdf_dpi=500,
        )
    )
