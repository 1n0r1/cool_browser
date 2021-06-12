from pyfiglet import Figlet
from plumbum import cli
from questionary import prompt
from os.path import expanduser
import pathlib
import os, sys
import subprocess

def print_banner(text):
    print(Figlet(font='slant').renderText(text))

def get_files(path): 
    files = os.listdir(path)
    files.sort()
    return files

def generate_choices(files):
    a = []
    a.append({'name': "Exit"})
    a.append({'name': "Change directory to current..."})
    a.append({'name': "..."})
    a.append({'name': "Create new folder..."})
    a.append({'name': "Create new file..."})
    for file in files:
        a.append({'name': file.strip()})
    return a

def generate_question(files, t):
    return [{
        'type': 'select',
        'name': 'files',
        'message': str(t),
        'choices': generate_choices(files)
    }]

def set_name():
    return [{
        'name':'files',
        'type': 'text',
        'message': 'Type name'
    }]

class CoolBrowser(cli.Application):
    VERSION = "1.3"

    def main(self):
        current_path = pathlib.Path(expanduser("~"))

        print_banner("Cool Browser")
        while (True):
            files = get_files(current_path)
            question = generate_question(files, current_path)
            answers = prompt(question)
            ans = answers['files']
            if (ans == "Exit"):
                return 0
            if (ans == "Change directory to current..."):
                os.chdir(current_path)
                os.system("pwd")
                os.system("/bin/bash")
            if (ans == "..."):
                current_path = current_path.parent.absolute()
                continue
            if (ans == "Create new folder..."):
                name = set_name()
                nname = prompt(name)
                os.mkdir(pathlib.Path(str(current_path) + "/" + nname['files']))
                continue
            if (ans == "Create new file..."):
                name = set_name()
                nname = prompt(name)
                pathlib.Path(str(current_path) + "/" + nname['files']).touch()
                continue
            selected = pathlib.Path(str(current_path) + "/" + ans)
            if os.path.isdir(selected):
                current_path = selected

if __name__ == "__main__":
    CoolBrowser()


### TESTS

def test_generate_question():
    files = ["best.rb", "good.kt", "small.py"]
    question = generate_question(files)
    assert len(question) == 1, "has to be one question"
    assert question[0]['type'] == 'select', "only 1 option is allowed"
    assert len(question[0]['choices']) == len(files) + 4, "same number of choices as files plus 4 options"