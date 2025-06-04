#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
from openai import OpenAI # type: ignore

client = OpenAI() # type: ignore
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
        return f"Error: {e}"

def main():
    print("\n")

    project_root = Path(os.getenv("PROJECT_ROOT", "."))
    lsbio_path = project_root / "tools" / "lsbio.py"
    result = subprocess.run(["python3", str(lsbio_path)], capture_output=True, text=True)
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