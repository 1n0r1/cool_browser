from pyfiglet import Figlet
from plumbum import cli
from questionary import prompt
from os.path import expanduser
import pathlib
import os, sys, fnmatch
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
    a.append({'name': "Search..."})
    for file in files:
        a.append({'name': file.strip()})
    return a

def generate_search_choices(files):
    a = []
    a.append({'name': "Exit"})
    a.append({'name': "Cancel"})
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

def generate_search_question(files, t):
    return [{
        'type': 'select',
        'name': 'files',
        'message': str(t),
        'choices': generate_search_choices(files)
    }]

def set_name():
    return [{
        'name':'files',
        'type': 'text',
        'message': 'Type name'
    }]

def display_browser(ppath):
    files = get_files(ppath)
    question = generate_question(files, ppath)
    answers = prompt(question)
    return answers['files']

def cd_to(pathh):
    os.chdir(pathh)
    os.system("pwd")
    os.system("/bin/bash")

def searchh(p, pathh):
    result = []
    for root, dirs, files in os.walk(pathh):
        for name in files:
            if p.lower() in name.lower():
                result.append(os.path.join(root, name))
        for name in dirs:
            if p.lower() in name.lower():
                result.append(os.path.join(root, name))
    return result

def display_search(pathh):
    nname = set_name()
    pattern = prompt(nname)

    result = searchh(pattern['files'], pathh)
    result.sort()

    question = generate_search_question(result, pathh)

    answers = prompt(question)
    if (answers['files'] == "Exit"):
        return -1
    if (answers['files'] == "Cancel"):
        return pathh
    if (os.path.isdir(answers['files'])):
        return answers['files']
    elif (os.path.isdir(pathlib.Path(answers['files']).parent.absolute())):
        return pathlib.Path(answers['files']).parent.absolute()
    return -1
    
class CoolBrowser(cli.Application):
    VERSION = "4"
    ch_dir = cli.Flag(['cd'], help="Also cd to current dir when you exit")
    homedir = cli.Flag(['home'], help="Start browser at home directory")

    def main(self):
        if (self.homedir):
            current_path = pathlib.Path(expanduser("~"))
        else:
            current_path = pathlib.Path(__file__).parent.absolute()
        print_banner("Cool Browser")

        while (True):
            ans = display_browser(current_path)
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
            if (ans == "Search..."):
                current_path = display_search(current_path)
                if (current_path == -1):
                    return 0
                current_path = pathlib.Path(current_path)
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
    assert len(question[0]['choices']) == len(files) + 5, "same number of choices as files plus 5 options"

def test_cd_to():
    current_path = pathlib.Path(os.getcwd())
    filepath = current_path

    cd_to(current_path.parent.absolute())
    current_path = os.getcwd()

    assert current_path != filepath