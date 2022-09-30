import os
from typing import List, Dict, Any
from prettytable import PrettyTable

from etc import (download_files, 
                create_folders,
                get_target_file)

def get_file_lines(file: str) -> List[str]:
    # file locations must be separated by new line in text file
    with open(file, 'r') as f:
         return [line.strip() for line in f.readlines()]

def get_folder_files(folder: str):
    return [os.path.join(folder, file) for file in next(os.walk(folder))[2]]

def get_file_lines(file: str) -> List[str]:
    # file locations must be separated by new line in text file
    with open(file, 'r', encoding='utf8') as f:
         return [line.strip() for line in f.readlines() if not line.startswith('#')]

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
        return f'ASK: {dct_rst["list"]}'
    elif dct_rst['type'] == 'CONSTRUCT':
        return dct_rst['str']
    return get_pretty_str(dct_rst['header'], rows=dct_rst['list'])

def get_pretty_str(header: List[str], rows: List[str], delim: str='\u2312'):
    x = PrettyTable(header=False)
    x.header=True
    x.field_names = ['#', *header]
    for i, line in enumerate(rows, start=1):
        x.add_row([i,*line.split(delim)]) if delim else  x.add_row([i,*line])
    x.align = "l"
    return x.get_string()


def save_and_update_files(local_path: str, files: List[str], overwrite: bool) -> List[str]:
        # create local store folder(s), if not yet exist(s)
        create_folders(local_path, os.getcwd())
        local_path = os.path.join(local_path)

        download_files(files, local_path, overwrite)
        # replace remote files with local files
        return get_files(local_path)

def get_files(file_folder: str, ext: str ='') -> List[str]:
    # return file directories
    root, dirs , files = next(os.walk(file_folder))
    return [os.path.join(root, file) for file in files if file.endswith(ext)]


def get_queries(query: str, idm: str='') -> List[str]:
    create_folders('requests', os.getcwd()) 
    create_folders('solutions', os.getcwd())
    f_req = os.path.join(os.getcwd(), 'requests')
    if idm: f_req = os.path.join(f_req, idm)

    if query == 'all':
        return get_folder_files(f_req)
   
    if not query.endswith('.rq'): query = f'{query}.rq'
    return [os.path.join(f_req, query)]

def get_sol_query(q: str) -> str:
    head, tail = os.path.split(q)
    return os.path.join(os.getcwd(), 'solutions', tail)

def create_result_row(d_overview: Dict[str, bool], lst_queries: List[str]) -> List[str]:
    l = []
    for q in lst_queries:
        passed = ('FAILED', 'PASSED')[int(d_overview[q])]if q in d_overview.keys() else 'NA'
        l.append(passed)
    return l

def create_overview_file(lst_columns: List[str], rows: List[List[str]], ts: str) -> None:
    header = ['IDM', 'PASSED', *lst_columns]
    content = get_pretty_str(header, rows, delim='')
    location = get_target_file('overview', '', ts, ext='.txt')
    save_file(location, content) 

def edit_files_file(idms: List[str], f_files: str, base: str, include_idm: bool, filenames: List[str]) -> None:
    # Overwrite files.txt
    files = [f'{base}{idm}/{name}' for idm in idms for name in filenames] if include_idm else [f'{base}{name}' for name in filenames]
    save_file(f_files, '\n'.join(files), mode='w')