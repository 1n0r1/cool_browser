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

def cd_to(pathh):
    os.chdir(pathh)
    os.system("pwd")
    os.system("/bin/bash")

class CoolBrowser(cli.Application):
    VERSION = "3"
    ch_dir = cli.Flag(['cd'], help="Also cd to current dir when you exit")
    homedir = cli.Flag(['home'], help="Start browser at home directory")

    def main(self):
        if (self.homedir):
            current_path = pathlib.Path(expanduser("~"))
        else:
            current_path = pathlib.Path(__file__).parent.absolute()
        print_banner("Cool Browser")
        while (True):
            files = get_files(current_path)
            question = generate_question(files, current_path)
            answers = prompt(question)
            ans = answers['files']
            selected = pathlib.Path(str(current_path) + "/" + ans)

            if (ans == "Exit"):
                if (self.ch_dir):
                    cd_to(current_path)
                return 0
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
            if os.path.isdir(selected):
                current_path = selected

if __name__ == "__main__":
    CoolBrowser()


### TESTS

def test_generate_question():
    files = ["best.rb", "good.kt", "small.py"]
    question = generate_question(files,"")
    assert len(question) == 1, "has to be one question"
    assert question[0]['type'] == 'select', "only 1 option is allowed"
    assert len(question[0]['choices']) == len(files) + 4, "same number of choices as files plus 4 options"

def test_cd_to():
    current_path = pathlib.Path(os.getcwd())
    filepath = current_path

    cd_to(current_path.parent.absolute())
    current_path = os.getcwd()

    assert current_path != filepath