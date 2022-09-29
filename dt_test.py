import logging as log
from typing import Dict, List, Tuple
from file_handling import get_pretty_str, save_file
from rdflib_handling import execute_query
# XSD Schema replacement beachten, um ausgabe zu verkürzen
import os
import rdflib
from dt_check import DtSolutions



from file_handling import get_files, read_file


def create_full_dt_comp(location: str, idm: str , g: rdflib.Graph, dct_tests: Dict[str, Tuple[str, Dict[str,int]]]) -> None:
    # executed to check a single student in complete manner (columns: dt occurrences, rows: datatypes)
    header = ['dt', 'req', 'sol', 'dif']
    # TODO full comparison
    # rows_req, rows_sol, rows_dif = [], [], []
    # for name, (query, dct_sol) in dct_tests.items():
    #     dct_req= create_dct_dt(execute_query(g, query))
    #     rows_req.append([])
        

    # for k in sorted(dct_diff.keys()):
    #     rows.append([k, dct_req.get(k, 0), dct_sol.get(k, 0)], dct_diff[k])
        
    # content = get_pretty_str(header, rows=rows, delim='')
    # save_file(location, content)




def create_dt_row(g: rdflib.Graph, dct_tests: Dict[str, Tuple[str, Dict[str,int]]]) -> Dict[str, bool]:
    d = {}
    for name, (query, dct_sol) in dct_tests.items():
        dct_req= create_dct_dt(execute_query(g, query))
        d[name] = are_same_dcts(dct_sol, dct_req)
    return d


def create_dct_dt(rst: rdflib.query.Result) -> Dict[str, int]:
    # must be SELECT with var[0]: datatype, var[1]: # of occurences
    return {dt.toPython(): count.toPython() for dt, count in rst if dt}


def are_same_dcts(sol: Dict[str, int], req: Dict[str, int]) -> bool:
    return all([sol[k] == req.get(k, 0) for k in sol.keys()])

def get_diff_dct (one: Dict[str, int], other: Dict[str, int]) -> Dict[str, int]:
    # key: datatype ; value: # of occurences
    shared = {k: v - other.get(k,0) for k, v in one.items()}
    return other | shared


def get_dt_solutions() -> Dict[str, Dict[rdflib.URIRef, int]]:
    # return dict with k: query / var name, val: dict(k: datatype, val: #)
    return {k: v for k,v in DtSolutions.__dict__.items() if not k.startswith('__')}

def get_available_dt_query_files():
    # return SPARQL files in dt_check folder (full path)
    return get_files('dt_check', ext='rq')

def isolate_filename(name: str) -> str:
    return os.path.splitext(os.path.split(name)[1])[0]

def key_to_str(d: Dict[rdflib.URIRef, int]) -> Dict[str, int]:
    return {k.toPython() : v for k,v in d.items()}

def are_test_queries_complete(selected_tests: List[str], available_tests: List[str]) -> bool:
    return len(set(selected_tests).difference(set(available_tests))) == 0

def get_dt_dct_tests(all_tests: Dict[str, Dict[rdflib.URIRef, int]], dct_sols = get_dt_solutions()) -> Dict[str, Tuple[str, Dict[str,int]]]:
    d = {}
    for f_test in all_tests:
        name = isolate_filename(f_test)
        if name in dct_sols.keys():
            try:
                d[name] = (read_file(f_test), key_to_str(dct_sols[name]))
            except Exception as e:
                print('File could not be read')
        else:
            print('Test query does not exist')
    return d

# idm: str , g: rdflib.Graph, dct_tests: Dict[str, Tuple[str, Dict[str,int]]]) -> List[str]
def proceed_with_dt_check(g: rdflib.Graph) -> List[str]:
    avail_tests, dct_sols = get_available_dt_query_files(), get_dt_solutions()
    dct_tests = get_dt_dct_tests(avail_tests, dct_sols)
    return create_dt_row(g, dct_tests)
    #if not are_test_queries_complete(list(dct_sols.keys()), list(dct_tests.keys())):
    #    print('return or stop, lets see')
    

if __name__ == '__main__':
    pass