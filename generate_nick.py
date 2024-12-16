import os
import sys
import random

if hasattr(sys, '_MEIPASS'):
    russian_path_1 = os.path.join(sys._MEIPASS, "first.txt")
else:
    russian_path_1 = os.path.join(os.path.abspath('.'), "first.txt")
if hasattr(sys, '_MEIPASS'):
    russian_path_2 = os.path.join(sys._MEIPASS, "second.txt")
else:
    russian_path_2 = os.path.join(os.path.abspath('.'), "second.txt")

def generate():
    final_str = ""
    with open(russian_path_1, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        final_str += lines[random.randint(0, len(lines))].replace("\n", "")

    with open(russian_path_2, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        final_str += " " + lines[random.randint(0, len(lines))].replace("\n", "")
    return final_str


