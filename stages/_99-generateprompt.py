#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
from openai import OpenAI # type: ignore

PROJECT_ROOT  = os.environ['PROJECT_ROOT']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# For users without venv
api_key= None
if api_key == None and not OPENAI_API_KEY:
    api_path= os.path.join(PROJECT_ROOT, 'api_key')
    with open(api_path, 'r', encoding='utf-8') as f:
        api_key = f.read()
client = OpenAI(api_key= api_key) # type: ignore

from stages.utils.dbcontroller import get_val, update_db

def ask_chatgpt(question: str, model: str = "gpt-4.1") -> str:
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

    project_root = Path(os.getenv("PROJECT_ROOT", "."))
    lsbio_path = project_root / "tools" / "lsbio.py"
    result = subprocess.run(["python3", str(lsbio_path)], capture_output=True, text=True)
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