#!/usr/bin/env python3
import os
import subprocess
from openai import OpenAI # type: ignore

api_key= None
if api_key== None:
    with open('api_key', 'r', encoding='utf-8') as f:
        api_key = f.read()
client = OpenAI(api_key= api_key) # type: ignore

from stages.utils.dbcontroller import get_val, update_db

def ask_chatgpt(question: str, model: str = "gpt-4.1") -> str:
    # api_key = os.getenv("OPENAI_API_KEY")
    # if not api_key:
    #     raise RuntimeError("OPENAI_API_KEY environment variable not set.")

    try:
        response = client.chat.completions.create(model=model,
        messages=[{"role": "user", "content": question}],
        temperature=0.7)
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("haha")
        return f"Error: {e}"

def main():
    print("\n")

    result = subprocess.run(["python3", "tools/lsbio.py"], capture_output=True, text=True)
    if result.returncode != 0:
        result = subprocess.run(["python", "tools/lsbio.py"], capture_output=True, text=True)

    if result.returncode != 0:
        print("Error running tools/lsbio.py:", result.stderr)
        return
    cols = result.stdout.strip()

    while True:
        biography = ask_chatgpt(f"Write a short biography (and write nothing else) for this citizen:\n {cols}")
        print(f"Biography: {biography}")
        choice = input("Accept (A), new generated suggestion (n) or enter name of your own (e)? ").strip() or 'A'
        if choice == 'e':
            biography = input("Enter biography manually: ")
        elif choice == 'A':
            break

    update_db('biography', biography)

if __name__ == "__main__":
    main()