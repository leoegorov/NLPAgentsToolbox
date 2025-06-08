import os
from pathlib import Path

project_root = str(Path(os.getenv("PROJECT_ROOT", ".")))

def readFile():
    fileName = project_root + '/jurorsFeatures.txt'
    with open(fileName, 'r', encoding='utf-8') as file:
        lines = [line.strip()[1:] for line in file if '-' in line[0]]
        return lines


_jurors = readFile()
_index = 0

def getLengthOfFeatures():
    return len(_jurors)

def get_next_features():
    global _index
    if _index >= len(_jurors):
        raise IndexError("No more jurors left in the list.")
    juror = _jurors[_index]
    _index += 1
    print(juror)
    return juror