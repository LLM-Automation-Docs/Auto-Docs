import os
import google.generativeai as genai

api_key = os.environ.get("LLAMA_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-1.5-flash')#gemini-1.5-flash


def generate_response(prompt):
    response = model.generate_content(prompt)
    return response.text

# Przykładowe użycie
"""while True:
    prompt = input("You: ")
    response_text = generate_response(prompt)
    print(f"Bot: {response_text}")

    # Dodaj wiadomość użytkownika i odpowiedź bota do historii konwersacji
    history.append(f"User: {prompt}")
    history.append(f"Bot: {response_text}")"""