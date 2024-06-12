import constants
from sys import exit
from os import path, listdir, mkdir, chdir
from typing import Iterable

_EXIT_FAILURE = 1
_EXIT_SUCCESS = 0

def identify_token(token:str) -> str:
    id_token = token in constants.TOKENS
    return token if id_token else constants.UNKNOWN_TOKEN

# Get all of the files that ends with .txt
def get_input_filenames(rpath:str = '.') -> list[str]:
    filenames = listdir(rpath)
    is_text_file = lambda filename: filename[-4:] == '.txt'
    input_filenames = list(filter(is_text_file, filenames))
    return input_filenames

def generate_output_filenames(filenames: list[str]|str, sufix: str) -> list[str]:
    rename_file = lambda filename: filename[0:-4] + f'{sufix}.txt'
    output_filenames = list(map(rename_file, filenames))
    return output_filenames

def dir_exists(dir_path:str) -> bool:
    exists = path.exists(path=dir_path)
    if exists:
        return True
    else:
        print(f'Diretório "{dir_path}" inexistente!')
        exit(_EXIT_FAILURE)

def _change_work_dir(work_path:str) -> bool:
    try:
        chdir(work_path)
        return True
    except PermissionError as ex:
        print(f'Você não possui permissão para acessar "{work_path}"')
        exit(_EXIT_FAILURE)

def change_dir(path:str) -> None:
    if dir_exists(dir_path=path):
        has_success_on_change_dir = _change_work_dir(path)
        if not has_success_on_change_dir:
            exit(_EXIT_FAILURE)
        
def is_empty_text_file(fd: int) -> bool:
    is_empty = not bool(path.getsize(fd))
    return is_empty


def endswithnewline(obj: list[str]) -> bool:
    ends = True if obj[-1] == '\n' else False
    return ends
