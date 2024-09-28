import json

from loguru import logger
from openai import AsyncOpenAI

from .llm_prompts.bielik import RULES


async def _get_ai_response(messages, callback=None):
    logger.info(f"Messages: {messages}")
    client = AsyncOpenAI(
        # base_url=os.environ["RUNPOD_BIELIK_URL"] + "/v1",
        # api_key=os.environ["RUNPOD_API_KEY"],
    )
    if callback:
        stream = await client.chat.completions.create(
            # model="speakleash/Bielik-11B-v2.3-Instruct",
            model="gpt-4o-2024-08-06",
            stream=True,
            messages=messages,
            temperature=0.0,
        )
        msg = ""
        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                msg += chunk.choices[0].delta.content
                await callback(msg)
        return msg
    else:
        res = await client.chat.completions.create(
            # model="speakleash/Bielik-11B-v2.3-Instruct",
            model="gpt-4o-2024-08-06",
            messages=messages,
            temperature=0.0,
        )
        return res.choices[0].message.content.strip()


async def get_ai_response(message, history, required_info, callback=None):
    system = (
        "Jesteś AI pomocnikiem podatnika. Zbierz informacje, które są potrzebne do wypełnienia wniosku. "
        "Odpowiadaj tylko i wyłącznie po polsku. Musisz zebrać następujące informacje: " + str(required_info) + ". "
    )
    system += "Zadawaj jedno pytanie na raz."

    user = message
    logger.info(f"History: {history}")
    return await _get_ai_response(
        [
            {"role": "system", "content": system},
            *history,
            {"role": "user", "content": user},
        ],
        callback=callback,
    )


async def parse_info(message, history, required_info) -> dict:
    system = (
        "Jesteś AI pomocnikiem podatnika. Zbierz informacje, które są potrzebne do wypełnienia wniosku. "
        "Odpowiadaj tylko i wyłącznie po polsku."
    )

    user = (
        "Oto informacje, które są potrzebne do wypełnienia wniosku: "
        + str(list(required_info.keys()))
        + ". Nie pytaj o nic więcej. "
        "Z wypowiedzi użytkownika wyciągnij podane informacje i wypisz je w formacie JSON. Odpowiadaj tylko i wyłącznie po polsku. "  # noqa: E501
        'Odpowiedz tylko w formacie JSON: {"nazwa_informacji": "wartość", "nazwa_informacji2": "wartość2"}. Jeżeli user nie podał żadnych informacji, zwróć pusty słownik: {}. \n'  # noqa: E501
        "Oto historia rozmowy: \n"
        + str("\n".join([f"- {msg['role']}: {msg['content']}" for msg in history]))
        + "\n- user: "
        + message
        + "\n"
        "Wyciągnij informacje z całej rozmowy."
    )

    res = await _get_ai_response(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
    )

    logger.info(f"Parsed info: {res}")

    # extract json from markdown
    res = res.replace("```json", "").replace("```", "").strip()

    return json.loads(res)


async def verify_if_necessary(message, history):
    system = (
        "Jesteś AI pomocnikiem podatnika. Sprawdź, czy użytkownik musi wypełniać wniosek PCC-3. "
        "Odpowiadaj tylko i wyłącznie po polsku."
    )

    user = (
        f"Oto zasady kiedy trzeba, a kiedy nie trzeba wypełniać wniosku: {RULES}. Oto najnowsza wiadomość użytkownika: `{message}`. "  # noqa: E501
        "Czy wiesz już, czy użytkownik musi wypełniać wniosek PCC-3?\n"
        "Odpowiedz tylko i wyłącznie jednym z: 'musi', 'nie musi', 'nie wiem'. Twoja odpowiedź będzie automatycznie parsowana."  # noqa: E501
    )

    res = await _get_ai_response(
        [
            {"role": "system", "content": system},
            *history,
            {"role": "user", "content": user},
        ]
    )
    logger.error(res)

    return res


async def question_if_necessary(message, history, callback=None):
    system = (
        "Jesteś AI pomocnikiem podatnika. Sprawdź, czy użytkownik musi wypełniać wniosek PCC-3. "
        "Odpowiadaj tylko i wyłącznie po polsku."
    )

    user = (
        f"Oto zasady kiedy trzeba, a kiedy nie trzeba wypełniać wniosku: {RULES}. Oto moja najnowsza wiadomość: `{message}`. "  # noqa: E501
        "Zadaj pytanie, które pomoże Ci ustalić czy muszę wypełniać formularz."
    )

    res = await _get_ai_response(
        [
            {"role": "system", "content": system},
            *history,
            {"role": "user", "content": user},
        ],
        callback,
    )

    return res


async def compute_tax_rate(message, history):
    system = "Jesteś AI pomocnikiem podatnika. " "Sprawdź jaka stawka podatku aplikuje się w sytuacji użytkownika"

    user = (
        f"Oto zasady wyliczania podatku od umów PCC: {RULES}. Oto moja najnowsza wiadomość: `{message}`. "  # noqa: E501
        "Wytłumacz, która stawka podatku jest zastosowana w sytuacji użytkownika."
        """Koniecznie odpisz w formacie:
        {
            "stawka": "stawka podatku, która się aplikuje",
            "argument": "wytłumaczenie dlaczego dana stawka się aplikuje"
        }
        Nie odbiegaj od powyższego formatu pod żadnym pozorem.
        """
    )

    res = await _get_ai_response(
        [
            {"role": "system", "content": system},
            *history,
            {"role": "user", "content": user},
        ],
    )
    res = res.replace("json", "").replace("```", "").strip()
    return json.loads(res)


async def rationale_why_not_necessary(message, history, callback=None):
    system = (
        "Jesteś AI pomocnikiem podatnika. Sprawdź, czy użytkownik musi wypełniać wniosek PCC-3. "
        "Odpowiadaj tylko i wyłącznie po polsku."
    )

    user = (
        f"Oto zasady kiedy trzeba, a kiedy nie trzeba wypełniać wniosku: {RULES}. Oto moja najnowsza wiadomość: `{message}`. "  # noqa: E501
        "Wytłumacz mi dlaczego nie muszę wypełniać wniosku."
    )

    res = await _get_ai_response(
        [
            {"role": "system", "content": system},
            *history,
            {"role": "user", "content": user},
        ],
        callback=callback,
    )

    return res
