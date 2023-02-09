import os
from datetime import datetime
from typing import List
import urllib.request
import rdflib
from logger import Logger
import logging as log

def download_files(file_locations: List[str], file_folder: str, overwrite: bool, logger: Logger) -> List[str]:
    """Downloads remote web resources to local path (see config.ini)
    :return: list of local files which could be downloaded from remote.
    """
    filenames = []
    for l in file_locations:
        if os.path.isfile(l):
            # if already local file
            filenames.append(l)
            continue

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
                logger.log_msg(e, f'Web resource "{l}" could not be saved at path "{local_file}"!' , log.WARNING)
                #log.warning(f'Web resource "{l}" could not be saved at path "{local_file}"!')
        if os.path.isfile(local_file):
            filenames.append(local_file)

    return filenames

def download_sparql_query(url: str, out: str, logger: Logger) -> None:
    """Downloads file from remote (here only sparql files)
    :param url: remote url where resource is retrieved
    :param out: local path where retrieved resource is saved
    """
    try:
        urllib.request.urlretrieve(url, out)
    except urllib.error.HTTPError as e:
        logger.log_msg(e, f'Could not download web resource at {url}', log.CRITICAL)
        #log.critical(f'Could not download web resource at {url}')

def get_timestamp() -> str:
    """return timestamp in format "yyyy-mm-dd hh-MM-ss"
    """
    now = str(datetime.now())
    return now.replace(':', '-')[:now.find('.')]

def get_target_file(query: str, type:str, timestamp: str, idm='', ext: str = '.tsv') -> str:
    """returns path where result should be saved.
    :param type: possible values (req -> requests)(sol -> solution)(dif -> difference between req and sol)
    """
    return f'{os.path.join(os.getcwd(),"results", os.path.splitext(os.path.split(query)[1])[0])}_{timestamp}{f"_{idm}" if idm else ""}{f"_{type}" if type else ""}{ext}'

def create_folders(path:str, base: str) -> None:
    """Creates recursively folder, if not yet exists (because rdflib serialization cannot handle nonexisting folders)
    """
    for dirname in reversed(get_dirs(path, [])):
        base = os.path.join(base, dirname)
        if not os.path.isdir(base):
            os.mkdir(base)

def get_dirs(path: str, lst: List[str]) -> List[str]:
    """returns recursively list of subdirectories for a path
    """
    head, tail = os.path.split(path)
    if not tail: return lst
    lst.append(tail)
    return get_dirs(head, lst)

def clear_folder(folder: str) -> None:
    """ deletes all files from a folder (here: result folder)
    """
    for f in os.listdir(folder):
        os.remove(os.path.join(folder, f))


