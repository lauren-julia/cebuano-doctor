import ollama

# Your installed Ollama models
TRANSLATOR_MODEL = "gemma4:latest"
MEDICAL_MODEL = "medgemma:4b"


def translate_to_english(cebuano_text):
    """Translate a Cebuano healthcare question into English."""

    prompt = f"""
Translate this Cebuano healthcare question into English.

IMPORTANT:
- Only translate.
- Do not answer the question.
- Keep the original meaning.
- Use clear and natural English.

Cebuano:
{cebuano_text}
"""

    response = ollama.chat(
        model=TRANSLATOR_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()


def get_medical_response(english_question):
    """Get a medical response from MedGemma."""

    prompt = f"""
You are a medical AI assistant.

Answer the following healthcare question in English.

Give a clear, helpful medical response.
Explain things in language that an ordinary person can understand.
Do not claim to be a human doctor.

If the symptoms could indicate an emergency, clearly recommend
seeking emergency medical care.

Healthcare question:
{english_question}
"""

    response = ollama.chat(
        model=MEDICAL_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()


def translate_to_cebuano(english_response):
    """Translate the medical response from English back to Cebuano."""

    prompt = f"""
Translate this medical response from English into natural Cebuano.

IMPORTANT:
- Preserve the medical meaning accurately.
- Do not add new medical information.
- Do not remove important information.
- Use Cebuano that is easy for an ordinary person to understand.
- Only provide the Cebuano translation.

English:
{english_response}
"""

    response = ollama.chat(
        model=TRANSLATOR_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()


def cebuano_doctor(question):
    """Run the complete Cebuano Doctor pipeline."""

    # STEP 1
    print("\n[1/3] Cebuano -> English")
    english_question = translate_to_english(question)

    print("\nEnglish translation:")
    print(english_question)

    # STEP 2
    print("\n[2/3] Asking MedGemma...")
    english_response = get_medical_response(english_question)

    print("\nEnglish medical response:")
    print(english_response)

    # STEP 3
    print("\n[3/3] English -> Cebuano")
    cebuano_response = translate_to_cebuano(english_response)

    return cebuano_response


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    print("======================================")
    print("          CEBUANO DOCTOR")
    print("======================================")
    print("Powered by Gemma 4 + MedGemma")
    print("Type 'quit' to exit.")

    while True:

        question = input("\nYou: ")

        if question.lower() == "quit":
            print("\nGoodbye!")
            break

        if not question.strip():
            print("Please enter a question.")
            continue

        try:

            answer = cebuano_doctor(question)

            print("\n======================================")
            print("       CEBUANO DOCTOR RESPONSE")
            print("======================================")
            print(answer)

        except Exception as error:

            print("\nSomething went wrong:")
            print(error)
