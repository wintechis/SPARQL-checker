import configparser
import argparse
import os
import logging as log
from typing import Any,  List, Union, Dict
import rdflib


from ldfu_wrapper import proceed_with_ldfu
from rdflib_handling import convert_rst_to_dict
from etc import get_timestamp
from file_handling import (create_folders,
                           get_file_lines,
                           get_folder_files,
                           get_target_file,
                           read_file,
                           save_and_update_files,
                           save_file,
                           save_pretty_file
                          )

def init() -> str:
    # ensure current working directory
    os.chdir(os.path.dirname(__file__))
    # load config file 
    config = load_config('config.ini')
    # set logging configurations
    return config,  configure_log(config['general']['log_file'])

def main(config: configparser.ConfigParser) -> None:
    # load remote file locations from files list into variable files
    file_path = os.path.join(config['data']['file_list'])
    files = get_file_lines(file_path) # all file iris

    # download files locally
    local_path = config['general']['local_store_path']
    if local_path:
        local_path, files = save_and_update_files(local_path, files, config['general'].getboolean('overwrite'))
    #ldfu only 
    #TODO add check if ldfu is installed

    # get parameters from console command
    args = get_args()
    # get request and solution query file paths
    
    # load rdf data
    if not args.ruleset: g = load_rdf_data(files)
    ts = get_timestamp()

    # change args.query to list of q_req if idm
    for q_req in get_queries(args.query):
        q_sol = get_sol_query(q_req)
        queries = [q_req, q_sol] if args.compare else [q_req]
        sol_file_exists = os.path.isfile(q_sol)
        if not sol_file_exists and args.compare:
            log.critical(f'Query file "{q_sol}" does not exist!')
            
        if args.ruleset:
            # only executed when -l, --ldfu
            proceed_with_ldfu(config['ldfu'], config['rulesets'], args.ruleset,
                              queries=queries, file_str=' '.join(files), timestamp=ts)
            return
        proceed_with_rdflib(g, queries, ts, sol_file_exists)


    #TODO add SPARQL comparison from helper tool
def proceed_with_rdflib(g: rdflib.Graph, q: List[str], ts: str, sol_file_exists: bool) -> None:
        # q: #0 q_req, #1 q_sol
        dct_req = execute_sparql(g, q[0])
        save_pretty_file(dct_req, get_target_file(q[0], 'req' , ts, '.txt'))

        if len(q) == 2 and sol_file_exists:
            dct_sol = execute_sparql(g, q[1])
            save_pretty_file(dct_sol, get_target_file(q[1], 'sol', ts, '.txt'))
            create_diff_file(get_target_file(q[0], 'dif', ts, '.txt'), dct_req, dct_sol)
            

def create_diff_file(diff_file: str, dct_req: Dict[str, Any], dct_sol: Dict[str, Any]) -> None:
    dct_plus = compare_results(dct_req, dct_sol, '+')
    dct_minus = compare_results(dct_sol, dct_req, '-')
    save_pretty_file(dct_plus, diff_file)
    save_file(diff_file, '\n\n', mode='a')
    save_pretty_file(dct_minus, diff_file, mode='a')

def execute_sparql(g: rdflib.Graph, q: str) -> Dict[str, Any]:
    rst_req = execute_query(g, read_file(q))
    dct_req = convert_rst_to_dict(rst_req)
    return dct_req

def load_config(config_file: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser(allow_no_value=True, interpolation=configparser.ExtendedInterpolation())
    config.read(config_file)
    return config

def configure_log(file: str) -> str:
    log_file = os.path.join(os.getcwd(), file)
    log.basicConfig(filename=log_file,
                        filemode='a',
                        level=log.ERROR,
                        format='%(asctime)s : %(levelname)8s : %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    return log_file

def get_args() -> argparse.Namespace:
    # return query path and applied ruleset
    parser = argparse.ArgumentParser(add_help=True)
    # positional arguments
    parser.add_argument("query", help='SPARQL file in folder "requests" to be executed. "all" executes entire folder.')
    # optional arguments
    parser.add_argument("-l", "--ldfu", dest='ruleset',choices=['all', 'owl', 'rdf', 'rdfs'], help="Select 'all', 'owl', 'rdf', 'rdfs'.")
    parser.add_argument("-i", "--idm", dest='idm', action="store_true", help="Create resource iris in files file from Idm file")
    parser.add_argument("-c", "--compare", dest='compare', action="store_true", help='SPARQL files in folder "requests" and "solutions" are executed.')
    
    args = parser.parse_args()
    return args

def get_queries(query: str) -> List[str]:
    #TODO move check to the beginning
    create_folders('requests', os.getcwd()) 
    create_folders('solutions', os.getcwd())
    f_req = os.path.join(os.getcwd(), 'requests')
    if query == 'all':
        return get_folder_files(f_req)
   
    if not query.endswith('.rq'): query = f'{query}.rq'
    return [os.path.join(f_req, query)]

def get_sol_query(q: str) -> str:
    head, tail = os.path.split(q)
    return os.path.join(os.path.dirname(head), 'solutions', tail)


# -----------------
def load_rdf_data(path: Union[str, List[str]]) -> rdflib.Graph():
    g = rdflib.Graph()
    if isinstance(path, str): path = [path]
    for p in path:
        try:
            g.parse(source=p)
        except Exception as e:
            log.error(e)
    return g 
     

def execute_query(g: rdflib.Graph, q: str) -> rdflib.query.Result:
    try:
        return g.query(q)
    except Exception as e:
        log.error(e)
        return rdflib.query.Result("ASK")

def compare_results(dct_one: Dict[str, Any], dct_other: Dict[str, Any], sign: str) -> Dict[str, Any]:
    lst = [f'{sign}\u2312{line}' for line in dct_one['list'] if line not in dct_other['list']]
    header = ['dif']
    header.extend(dct_one['header'])
    return {'header': header,
            'list': lst
        }






if __name__ == '__main__':
    config, log_file = init()
    n = get_file_lines(log_file)
    main(config)

    if n == get_file_lines(log_file):
        print('Program finished.')
    else:
        print('Program raised error(s). Please check the log file for more information.')