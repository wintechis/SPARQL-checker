from typing import Tuple, Dict, Any, List, Union
import rdflib
import logging as log

from etc import get_target_file
from file_handling import (read_file,
                           save_file,
                           save_pretty_file)


def proceed_with_rdflib(g: rdflib.Graph, q: List[str], ts: str, idm: str, sol_file_exists: bool) -> int:
        # q: #0 q_req, #1 q_sol
        n = 0
        dct_req = execute_sparql(g, q[0])
        save_pretty_file(dct_req, get_target_file(q[0], 'req' , ts, idm, '.txt'))

        if len(q) == 2 and sol_file_exists:
            dct_sol = execute_sparql(g, q[1])
            save_pretty_file(dct_sol, get_target_file(q[1], 'sol', ts,idm,  '.txt'))
            n = create_diff_file(get_target_file(q[0], 'dif', ts, idm, '.txt'), dct_req, dct_sol)
        return n

def create_diff_file(diff_file: str, dct_req: Dict[str, Any], dct_sol: Dict[str, Any]) -> int:
    dct_plus = compare_results(dct_req, dct_sol, '+')
    dct_minus = compare_results(dct_sol, dct_req, '-')
    save_pretty_file(dct_plus, diff_file)
    save_file(diff_file, '\n\n', mode='a')
    save_pretty_file(dct_minus, diff_file, mode='a')
    return len(dct_plus['list']) + len(dct_minus['list'])

def execute_query(g: rdflib.Graph, q: str) -> rdflib.query.Result:
    # move to rdf handling
    try:
        return g.query(q)
    except Exception as e:
        log.error(e)
        return rdflib.query.Result("ASK")

def execute_sparql(g: rdflib.Graph, q: str) -> Dict[str, Any]:
    # move to rdf handling
    rst_req = execute_query(g, read_file(q))
    dct_req = convert_rst_to_dict(rst_req)
    return dct_req

def convert_rst_to_dict(rst: rdflib.query.Result) -> Dict[str,Any]:
    d = {'header': 'ASK QUERY',
         'type': rst.type,
         'list'  : []}
    l = d['list']
    delim = '\u2312'
    if rst.type == 'ASK':
        l.append(rst.askAnswer)
        return d
    elif rst.type == 'CONSTRUCT':
         d['str']  = rst.serialize(format='ttl').decode(('utf-8')) 
         d['list'] = create_lst_from_construct(rst, delim)
         d['header'] = ['s', 'p', 'o']
         return d
    elif rst.type == 'SELECT':
        d['header'] = [var.toPython() for var in rst.vars]

    for row in rst:
        if rst.type == 'CONSTRUCT': # CONSTRUCT
            l.append(f'{delim}'.join(map(str,[val.toPython() for val in row])))
            continue
        #SELECT
        l.append(f'{delim}'.join(map(str,[val.toPython() for val in row.asdict().values()])))
    return d


def create_lst_from_construct(rst: rdflib.query.Result, delim: str) -> List[str]:
    # 
    return [f'{delim}'.join((s.toPython(), p.toPython(), o.toPython())) for (s, p, o) in rst]



def reduce_dt_str(dt: str) -> str:
    ns = {str(rdflib.XSD): 'XSD.', str(rdflib.RDF): 'RDF.'}
    for p in ns.keys():
        if dt.startswith(p):
            dt = ns[p] + dt[len(p):]
    return dt

def compare_results(dct_one: Dict[str, Any], dct_other: Dict[str, Any], sign: str) -> Dict[str, Any]:
    delimiter = '\u2312'
    lst = [f'{sign}{delimiter}{line}' for line in dct_one['list'] if line not in dct_other['list']]
    header = ['dif']
    header.extend(dct_one['header'])
    # if isinstance(dct_one['list'], str):
    #    lst = compare_construct_rst(dct_one['list'], dct_other['list'], sign, delimiter)
    if dct_one['type'] == 'CONSTRUCT': dct_one['type'] = 'SELECT' # Diff file for CONSTRUCT is same as SELECT
    return {'header': header,
            'list': lst,
            'type': dct_one['type']
        }

def load_rdf_data(path: Union[str, List[str]]) -> rdflib.Graph():
    g = rdflib.Graph()
    if isinstance(path, str): path = [path]
    for p in path:
        try:
            g.parse(source=p)
        except Exception as e:
            log.error(e)
    return g 
     