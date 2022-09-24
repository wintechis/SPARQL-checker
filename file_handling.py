import os
from typing import List, Dict, Any, Tuple

import rdflib
from prettytable import PrettyTable

def get_file_lines(file: str) -> List[str]:
    # file locations must be separated by new line in text file
    with open(file, 'r') as f:
         return [line.strip() for line in f.readlines()]

def get_folder_files(folder: str):
    return [os.path.join(folder, file) for file in next(os.walk(folder))[2]]

def get_file_lines(file: str) -> List[str]:
    # file locations must be separated by new line in text file
    with open(file, 'r', encoding='utf8') as f:
         return [line.strip() for line in f.readlines()]

def read_file(path: str) -> str:
    with open(path, 'r', encoding='utf8') as f:
        return f.read()

def save_file(location: str, content: str, mode: str='w') -> None:
    with open(location, mode, encoding='utf8') as f:
        f.write(content)

def save_pretty_file(dct_rst: Dict[str, Any], location: str, mode: str='w'):
    content = get_result_str(dct_rst)
    save_file(location, content, mode)

def get_result_str(dct_rst: Dict[str, Any]) -> str:
    if dct_rst['type'] == 'ASK':
        return f'ASK: {dct_rst["list"][0]}'
    elif dct_rst['type'] == 'CONSTRUCT':
        return dct_rst['list']
    x = PrettyTable(header=False)
    x.header=True
    x.field_names = ['#', *dct_rst['header']]
    for i, line in enumerate(dct_rst['list'], start=1):
        x.add_row([i,*line.split('\u2312')])
    x.align = "l"
    return x.get_string()

def get_target_file(query: str, type:str, timestamp: str, idm='', ext: str = '.tsv') -> str:
    return f'{os.path.join(os.getcwd(), "results", os.path.split(query)[1][:-3])}_{timestamp}{f"_{idm}" if idm else ""}_{type}{ext}'

def save_and_update_files(local_path: str, files: List[str], overwrite: bool) -> List[str]:
        # create local store folder(s), if not yet exist(s)
        create_folders(local_path, os.getcwd())
        local_path = os.path.join(local_path)

        download_files(files, local_path, overwrite)
        # replace remote files with local files
        return get_files(local_path)

def get_files(file_folder: str) -> List[str]:
    # return file directories
    root, dirs , files = next(os.walk(file_folder))
    return [os.path.join(root, file) for file in files]

def download_files(file_locations: List[str], file_folder: str, overwrite: bool) -> None:
    for l in file_locations:
        name = l[l.rfind('/') + 1:]
        pos_tilde = l.find('~')
        user = l[pos_tilde + 1: pos_tilde +9]
        local_file = os.path.join(  os.path.dirname(__file__),
                                    file_folder, 
                                    f'{user}_{name}')
        if not os.path.isfile(local_file) or overwrite:
            try:
                rdflib.Graph().parse(l).serialize(local_file)
            except Exception as e:
                print(f'Error for "{l}"', e)

def create_folders(path:str, base: str) -> None:
    for dirname in reversed(get_dirs(path, [])):
        base = os.path.join(base, dirname)
        if not os.path.isdir(base):
            os.mkdir(base)

def get_dirs(path: str, lst: List[str]) -> List[str]:
    head, tail = os.path.split(path)
    if not tail: return lst
    lst.append(tail)
    return get_dirs(head, lst)