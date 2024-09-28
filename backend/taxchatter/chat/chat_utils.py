from openai import AsyncOpenAI


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

async def get_ai_response(message, callback=None):
    system = "Jesteś AI pomocnikiem podatnika. Zbierz informacje, które są potrzebne do wypełnienia wniosku. "\
    "Odpowiadaj tylko i wyłącznie po polsku."

    user = message
    return await _get_ai_response([
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ], callback=callback)