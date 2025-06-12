#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
from openai import OpenAI # type: ignore
from stages.utils.dbcontroller import get_val, update_db
from tools.readFile import get_next_features

PROJECT_ROOT  = os.environ['PROJECT_ROOT']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# For users without venv
api_key= None
if api_key == None and not OPENAI_API_KEY:
    api_path= os.path.join(PROJECT_ROOT, 'api_key')
    with open(api_path, 'r', encoding='utf-8') as f:
        api_key = f.read()
client = OpenAI(api_key= api_key) # type: ignore

def ask_chatgpt(question: str, model: str = "gpt-4.1") -> str:
    try:
        response = client.chat.completions.create(model=model,
        messages=[{"role": "user", "content": question}],
        temperature=0.7)
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"\033[93mError: {e}\033[0m"

def main():
    project_root = Path(os.getenv("PROJECT_ROOT", "."))
    lsbio_path = project_root / "tools" / "lsbio.py"
    result = subprocess.run(["python3", str(lsbio_path)], capture_output=True, text=True)
    if result.returncode != 0:
        result = subprocess.run(["python", "tools/lsbio.py"], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"\033[93mError running tools/lsbio.py: {result.stderr}\033[0m")
        return
    cols = result.stdout.strip()

    while True:
        msgToChatGPT = f"Write a short biography (and write nothing else) for this citizen:\n {cols}. " \
                       f"I have some new features I want this biography to have, if you have a contradiction " \
                       f"from previous data, please take the new data I will give you. Make sure that all the story " \
                       f"makes sense. Change it to make sense if there is some contradiction." \
                       f"If you want you can change the name according to the gender. I want this biography to be:" \
                       f"{get_next_features()}"

        biography = ask_chatgpt(msgToChatGPT)
        print(f"Biography: {biography}")
        choice = input("\nAccept (A), new generated suggestion (n), enter name of your own (e)? if you want to "
                       "change something specific: just write it in a simple sentence (Example: Please change his "
                       "name to be ..):\n ").strip() or 'A'
        if choice == 'e':
            biography = input("Enter biography manually: ")
        elif choice == 'A':
            break
        elif choice == 'n':
            continue
        else:
            msgToChatGPT = f"I will provide to you a biography and a changing requirement. Please change the biography" \
                           f" according to the new requirement. Make sure that all the story makes sense. Change " \
                           f"it to make sense if there is some contradiction" \
                           f"Only write the new biography and nothing else. " \
                           f"Biography : {biography}" \
                           f"New requirement: {choice}" \
                           f"If the requirement is meaningless just return the previous biography."
            biography = ask_chatgpt(msgToChatGPT)
            print(f"Changed Biography: {biography}")
            break

    update_db('biography', biography)

if __name__ == "__main__":
    main()