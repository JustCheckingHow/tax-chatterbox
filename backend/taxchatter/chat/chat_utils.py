import json
from datetime import datetime

import httpx
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from loguru import logger
from openai import AsyncOpenAI

from .llm_prompts.bielik import RULES


async def _get_ai_response(messages, callback=None):
    client = AsyncOpenAI(
        # base_url="https://gaiuslexopenaisponsored.openai.azure.com/openai/deployments/gpt-4o",
        # api_key=os.environ["AZURE_API_KEY"],
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


async def get_ai_response(message, history, required_info, obtained_info, callback=None):
    system = (
        f"Jest {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. Jesteś AI pomocnikiem podatnika. "
        "Zbierz informacje, które są potrzebne do wypełnienia wniosku. "
        "Odpowiadaj tylko i wyłącznie po polsku. Musisz zebrać następujące informacje: " + str(required_info) + ". "
        "Oto informacje, które użytkownik już podał: " + str(obtained_info) + ". "
    )
    system += "Zadawaj jedno pytanie na raz."

    user = message
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

    history_str = (
        f"Jest {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. Oto historia wiadomości: "
        + "\n".join([f"- {msg['role']}: ```{msg['content']}```" for msg in history])
        + ". \n"
    )

    user = (
        "Oto informacje, które są potrzebne do wypełnienia wniosku: "
        + str(required_info)
        + ". Nie pytaj o nic więcej. "
        "Z wypowiedzi użytkownika wyciągnij podane informacje i wypisz je w formacie JSON. Odpowiadaj tylko i wyłącznie po polsku. "  # noqa: E501
        'Odpowiedz tylko w formacie JSON: {"nazwa_informacji": "wartość", "nazwa_informacji2": "wartość2"}. Jeżeli user nie podał żadnych informacji, zwróć pusty słownik: {}. \n'  # noqa: E501
        f"{history_str}\n" + "Wyciągnij informacje z całej rozmowy."
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


async def recognize_question(message, history):
    history.append({"role": "user", "content": message})

    logger.info(f"History: {history}")

    system = (
        "Jesteś AI pomocnikiem podatnika. Rozpoznaj intencję użytkownika. " "Odpowiadaj tylko i wyłącznie po polsku."
    )

    user = (
        "Oto historia wiadomości: " + "\n".join([f"- {msg['role']}: {msg['content']}" for msg in history]) + ". "  # noqa: E501
        "Użytkownik pyta o coś związanego z podatkami, opisuje sytuację, wita się, czy pyta o coś niezwiązanego? \n"
        "Odpisz tylko jednym słowem: 'pytanie', 'sytuacja', 'powitanie', 'inne'."
    )

    res = await _get_ai_response(
        [
            {"role": "system", "content": system},
            *history,
            {"role": "user", "content": user},
        ],
    )

    return res


async def refuse_to_answer(message, history, callback=None):
    history.append({"role": "user", "content": message})

    system = "Jesteś AI pomocnikiem podatnika. Odpowiadaj tylko i wyłącznie po polsku."
    history_str = (
        "Oto historia wiadomości: " + "\n".join([f"- {msg['role']}: {msg['content']}" for msg in history]) + ". \n"
    )

    logger.info(f"History: {history_str}")

    user = (
        history_str
        + "Użytkownik pyta o coś niezwiązanego z tematem. Grzecznie odmów odpowiedzi. Nie podaj żadnych informacji."
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


async def scrap_ddgo_for_info(message, history, callback=None):
    history = history[-6:]
    history.append({"role": "user", "content": message})

    history_str = (
        "Oto historia wiadomości: " + "\n".join([f"- {msg['role']}: {msg['content']}" for msg in history]) + ". \n"
    )

    system = "Jesteś AI pomocnikiem podatnika. Odpowiadaj tylko i wyłącznie po polsku."

    user = history_str + "Użytkownik zadał pytanie. Przygotuj zapytanie do wyszukiwarki DuckDuckGo."

    query = await _get_ai_response(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )

    ddg_results_content = []

    ddg_results = DDGS().text(query + " site:podatki.gov.pl", region="pl-pl", max_results=3)
    for result in ddg_results:
        markdown_content = await _scrap_website_to_markdown(result["href"])
        ddg_results_content.append(f"---\nURL: {result['href']}\n\n{markdown_content}\n---\n")

    content = "\n".join(ddg_results_content)

    user = (
        history_str + "Oto wyniki wyszukiwania DuckDuckGo: " + content + ". \n"
        "Użytkownik zadał pytanie. Odpowiedz na nie na podstawie wyników wyszukiwania. Cytuj źródła."
    )

    res = await _get_ai_response(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        callback=callback,
    )

    return res


async def _scrap_website_to_markdown(url: str) -> str:
    logger.info(f"Scraping {url}")
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text()[:10000]
