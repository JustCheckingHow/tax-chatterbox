from openai import AsyncOpenAI
import json
from loguru import logger


async def _get_ai_response(messages, callback=None):
    client = AsyncOpenAI()
    if callback:
        stream = await client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            stream=True,
            messages=messages,
            temperature=0.0
        )
        msg = ""
        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                msg += chunk.choices[0].delta.content
                await callback(msg)

    res = await client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=messages,
        temperature=0.0
    )
    return res.choices[0].message.content.strip()

async def get_ai_response(message, required_info, callback=None):
    system = "Jesteś AI pomocnikiem podatnika. Zbierz informacje, które są potrzebne do wypełnienia wniosku. "\
    "Odpowiadaj tylko i wyłącznie po polsku. Musisz zebrać następujące informacje: " + str(list(required_info.keys())) + ". "
    system += "Zadawaj jedno pytanie na raz."

    user = message
    return await _get_ai_response([
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ], callback=callback)

async def parse_info(message, required_info) -> dict:
    system = "Jesteś AI pomocnikiem podatnika. Zbierz informacje, które są potrzebne do wypełnienia wniosku. "\
    "Odpowiadaj tylko i wyłącznie po polsku."

    user = "Oto informacje, które są potrzebne do wypełnienia wniosku: " + str(list(required_info.keys())) + ". "\
    "Z wypowiedzi użytkownika wyciągnij podane informacje i wypisz je w formacie JSON. Odpowiadaj tylko i wyłącznie po polsku. " \
    "Odpowiedz tylko w formacie JSON: {'nazwa_informacji': 'wartość', 'nazwa_informacji2': 'wartość2'}. \nOto wypowiedź użytkownika: ```\n" + message + "\n```"

    res = await _get_ai_response([
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ])

    logger.info(f"Parsed info: {res}")

    # extract json from markdown
    res = res.replace("```json", "").replace("```", "").strip()

    return json.loads(res)