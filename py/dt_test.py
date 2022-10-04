from typing import Dict, List, Tuple
from file_handling import get_pretty_str, save_file
from rdflib_handling import execute_query, reduce_dt_str
import os
import rdflib
from dt_check import DtSolutions
from logger import Logger
import logging as log

from file_handling import get_files, read_file


def create_full_dt_comp(location: str, idm: str , g: rdflib.Graph, dct_tests: Dict[str, Tuple[str, Dict[str,int]]], logger: Logger) -> None:
    """Saves datatype comparisons between result set and expected datatype occurences.

    :param location: path to file where comparison is saved
    :param idm: student identifier (8 chars)
    :param g: RDF graph containing all triples from considered RDF documents.
    :param dct_tests: dict with k: query name, val: (query string, dict with k: datatype name and val: # occurences)
    :param logger: log instance
    """
    # executed to check a single student in complete manner (columns: dt occurrences, rows: datatypes)
    header = ['dt', 'req', 'sol', 'dif']
    dist = '\n'*2
    content = f'IDM: {idm}'
    for name, (query, dct_sol) in dct_tests.items():
        dct_req= create_dct_dt(execute_query(g, query, logger))
        dct_diff = get_diff_dct(dct_sol, dct_req)
        rows = []
        for k in dct_diff.keys():
           rows.append([reduce_dt_str(k), dct_req.get(k, 0), dct_sol.get(k, 0), dct_diff[k]])
        content += f'{dist}Datatype Check: {name}\n{get_pretty_str(header, rows, delim="")}'
    save_file(location, content)

        
def create_dt_row(g: rdflib.Graph, dct_tests: Dict[str, Tuple[str, Dict[str,int]]], logger: Logger) -> Dict[str, bool]:
    """Create dictionary that contains True/False values for queries. It is referred to as "row"
    , because the row will be formed by sorting the dict keys.

    :param g: RDF graph containing all triples from considered RDF documents.
    :param dct_tests: dict with k: query name, val: (query string, dict with k: datatype name and val: # occurences)
    :param logger: log instance

    :return: dict with k: query name and val: True when datatype result matches expected datatype result
    """
    d = {}
    for name, (query, dct_sol) in dct_tests.items():
        dct_req= create_dct_dt(execute_query(g, query, logger))
        d[name] = are_same_dcts(dct_sol, dct_req)
    return d


def create_dct_dt(rst: rdflib.query.Result) -> Dict[str, int]:
    """Transforms rdflib Result to Python dictionary.

    :param rst: Result with the two variables dt (datatype) and count (# occurences)
    :return: dict with k: datatype name, val: number of occurences
    """
    # must be SELECT with var[0]: datatype, var[1]: # of occurences
    return {dt.toPython(): count.toPython() for dt, count in rst if dt}


def are_same_dcts(sol: Dict[str, int], req: Dict[str, int]) -> bool:
    """Returns True, if dictionaries contain same pairs.

    :param sol: expected solution (k: datatype, val: #)
    :param req: result from executed query (k: datatype, val: #)
    :return: True when both contain same pairs
    """
    b_sol = all([sol[k] == req.get(k, 0) for k in sol.keys()])
    b_req  = all([req[k] == sol.get(k, 0) for k in req.keys()])
    return b_sol and b_req

def get_diff_dct (one: Dict[str, int], other: Dict[str, int]) -> Dict[str, int]:
    """Returns dictionary with all keys and the occurences difference 
    from :one compared to :other.

    :param one: dict[dt, #] 
    :param other: dict[dt, #]
    :return: dict containing keys of both 
    """
    shared = {k: v - other.get(k,0) for k, v in one.items()}
    return other | shared


def get_dt_solutions() -> Dict[str, Dict[rdflib.URIRef, int]]:
    """Retrieves expected datatype dictionaries from DtSolutions (see dt_check/__init__.py)
    
    :return: dictionary using datatype URIRef as keys
    """
    # return dict with k: query / var name, val: dict(k: datatype, val: #)
    return {k: v for k,v in DtSolutions.__dict__.items() if not k.startswith('__')}

def get_available_dt_query_files() -> List[str]:
    """return SPARQL files in dt_check folder (full path). SPARQL files must
    have the file extension "rq".
    """
    return get_files('dt_check', ext='rq')

def isolate_filename(name: str) -> str:
    """returns filename without file extension
    """
    return os.path.splitext(os.path.split(name)[1])[0]

def key_to_str(d: Dict[rdflib.URIRef, int]) -> Dict[str, int]:
    """returns new dictionary where originally datatype URIRefs 
    were converted to string.
    """
    return {k.toPython() : v for k,v in d.items()}

def are_test_queries_complete(selected_tests: List[str], available_tests: List[str]) -> bool:
    """returns True, if all DtSolution dictionaries have a matching query file.
    """
    return len(set(selected_tests).difference(set(available_tests))) == 0

def get_dt_dct_tests(all_tests: Dict[str, Dict[rdflib.URIRef, int]], dct_sols, logger: Logger) -> Dict[str, Tuple[str, Dict[str,int]]]:
    """returns dict with k: query name, val: (query string, dict with k: datatype name and val: # occurences)
    """
    d = {}
    for f_test in all_tests:
        name = isolate_filename(f_test)
        if name in dct_sols.keys():
            try:
                d[name] = (read_file(f_test), key_to_str(dct_sols[name]))
            except Exception as e:
                logger.log_msg(e, f'File {f_test} could not be read.', log.Error)
        else:
            logger.log_msg(FileNotFoundError, f'File {name} does not exist.', log.Error)
    return d

def proceed_with_dt_check(g: rdflib.Graph, target_file: str, idm: str, logger: Logger) -> Dict[str, bool]:
    """executes datatype comparison, saves single test comparison file and returns dict for overview row.
    """
    avail_tests, dct_sols = get_available_dt_query_files(), get_dt_solutions()
    dct_tests = get_dt_dct_tests(avail_tests, dct_sols, logger)
    create_full_dt_comp(target_file, idm, g, dct_tests, logger) 
    
    return create_dt_row(g, dct_tests, logger)

if __name__ == '__main__':
    print('see "python checker.py --help" for command overview.')