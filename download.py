import os
from typing import List
import urllib.request
import logging as log
import rdflib


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


def download_sparql_query(url: str, out: str) -> None:
    try:
        urllib.request.urlretrieve(url, out)
    except urllib.error.HTTPError:
        log.critical(f'Could not download web resource at {url}')
