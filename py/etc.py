import os
from datetime import datetime
from typing import List
import urllib.request
import rdflib
import logging as log

def download_files(file_locations: List[str], file_folder: str, overwrite: bool) -> None:
    for l in file_locations:
        name = l[l.rfind('/') + 1:]
        pos_tilde = l.find('~')
        user = l[pos_tilde + 1: pos_tilde +9]
        local_file = os.path.join(  os.getcwd(),
                                    file_folder, 
                                    f'{user}_{name}')
        if not os.path.isfile(local_file) or overwrite:
            try:
                rdflib.Graph().parse(l).serialize(local_file)
            except Exception as e:
                print(f'Error for "{l}"', e)

def download_sparql_query(url: str, out: str) -> None:
    try:
        urllib.request.urlretrieve(url, out)
    except urllib.error.HTTPError:
        log.critical(f'Could not download web resource at {url}')

def get_timestamp() -> str:
    # return yyyy-mm-dd hh-MM-ss
    now = str(datetime.now())
    return now.replace(':', '-')[:now.find('.')]

def get_target_file(query: str, type:str, timestamp: str, idm='', ext: str = '.tsv') -> str:
    return f'{os.path.join(os.getcwd(),"results", os.path.splitext(os.path.split(query)[1])[0])}_{timestamp}{f"_{idm}" if idm else ""}{f"_{type}" if type else ""}{ext}'

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

def clear_folder(folder: str) -> None:
    for f in os.listdir(folder):
        os.remove(os.path.join(folder, f))