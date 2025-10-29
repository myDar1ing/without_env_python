import os, json, requests
from dotenv import load_dotenv
load_dotenv()
#meme
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL= os.getenv("OPENAI_MODEL", "gpt-4o-mini")
API_KEY= os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY не задан в окружении")

CHAT_URL = f"{BASE_URL}/chat/completions"

SYSTEM_PROMPT = (
    "Ты — дружелюбный репетитор по биологии для школьников. "
    "Объясняй просто и коротко. Если вопрос неоднозначен — уточни 1 вещь. "
    "Отвечаешь вопросам только по биологии, если вопрос не касается этого, попроси пользователя чтоб задал вопрос по биологии"
    "Дай решение/объяснение в 2–4 шагах и итоговый ответ. "
    "Добавляй 1 мини-совет по теме в конце (1 строка)."
)

def ask_llm(question: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": question},
        ],
        "temperature": 0.2,
    }
    try:
        resp = requests.post(
            CHAT_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            data=json.dumps(payload),
            timeout=60
        )
        # resp.raise_for_status()
        obj = json.loads(resp.text)
        print(obj)
        return obj["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        return f"Ошибка запроса: {e}"

def main():
    print("🧬 Биобот запущен. Спроси что угодно по биологии (или /exit):")
    while True:
        try:
            q = input("\nТы: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nПока! 👋"); break
        if not q: 
            continue
        if q.lower() in ("/exit", "exit", "quit"):
            print("Пока! 👋"); break
        print(f"Бот: {ask_llm(q)}")

if __name__ == "__main__":
    main()