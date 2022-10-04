import argparse
from genericpath import isfile
import os
import logging as log
from typing import  List, Dict, Tuple

import sys
sys.path.append('py')

from py.config import Config
from py.logger import Logger
from py.ldfu_wrapper import proceed_with_ldfu
from py.rdflib_handling import (load_rdf_data,
                                proceed_with_rdflib
                                )
from py.etc import (clear_folder, get_timestamp,
                    get_target_file,
                    download_sparql_query
                    )
from py.dt_test import proceed_with_dt_check
from py.file_handling import (  create_folders,
                                get_file_lines,
                                get_queries,
                                get_sol_query,
                                save_and_update_files,
                                create_result_row,
                                create_overview_file,
                                edit_files_file
                            )


def main(config: Config, logger: Logger) -> None:
    """main function running idm loop
    """
    args    = get_args()
    f_idm   = config.idms_file 
    f_files = config.files_file 
    idms    = get_file_lines(f_idm)

    if args.idm:
        idms = [args.idm]
        args.single = True

    ALL_ONCE = not args.single

    ts = get_timestamp()
    is_dt_test = args.query.lower() == 'test'
    
    if args.query.lower() == 'all':
        lst_sol_queries = sorted(os.listdir(os.path.join(os.getcwd(), 'solutions')) , reverse=True)
    else:
        lst_sol_queries = [f'{os.path.splitext(args.query)[0]}.rq']
    
    lst_overall = []
    for idm in idms:
        # create idm-only files and return overview dictionary
        d_overview = run(args, config, idms if ALL_ONCE else [idm], f_files, ts, logger)
        # change column fields for overview, if datatype test
        if is_dt_test: lst_sol_queries = d_overview.keys()
        # return list where indices represent a solution query
        row_rst = create_result_row(d_overview, lst_sol_queries)
        # convert bool values to description in list
        row = ['ALL' if ALL_ONCE else idm, f'{row_rst.count("PASSED")}/{len(row_rst)}', *row_rst]
        lst_overall.append(row)
        if ALL_ONCE: break
    if args.compare:
        create_overview_file(lst_sol_queries, lst_overall, ts)


def run(args: argparse.Namespace, config: Config, idms: List[str], f_files: str, ts: str, logger: Logger) -> Dict[str, str]:
        """execution sequence for each idm. Only when -s flag is not set, all idms are passed.
        """
        d = {}
        if args.update:
            # Update files.txt
            edit_files_file(idms, f_files, config.remote_base_url, config.include_idms, config.filenames)
        # load remote file locations from files list into variable files
        files = get_file_lines(f_files) # all file iris
        cur_idm = idms[0] if args.single else ['all']
        # download files locally
        local_path = os.path.join(config.local_store_path, cur_idm)
        if local_path !=cur_idm:
            files, ignored_files = save_and_update_files(local_path, files, config.overwrite, logger)
            for f in ignored_files:
                logger.log_msg(Exception, f'"{f}" is a local file, which is not included in the files list.', log.INFO)
      
        # load rdf data / add if check
        if not args.ruleset: g = load_rdf_data(files)
        
        if args.query.lower() == 'test':
            target_file = get_target_file('dt', '', ts, cur_idm, ext='.txt')
            return proceed_with_dt_check(g, target_file, cur_idm, logger)
        # change args.query to list of q_req if idm
        queries = get_queries(args.query)
        for q_req in queries:
            if args.single:
                url     = config.get_remote_query_url(cur_idm, os.path.split(q_req)[1])
                q_req  =  config.get_local_query_path(cur_idm, os.path.split(q_req)[1])
                create_folders(cur_idm, os.path.join(os.getcwd(), 'requests'))
                if not (os.path.isfile(q_req) and not config.overwrite):
                    download_sparql_query(url, q_req, logger)
            if not os.path.isfile(q_req): 
                continue
            q_sol = get_sol_query(q_req)
            pair = [q_req, q_sol] if args.compare else [q_req]
            sol_file_exists = os.path.isfile(q_sol)
            if not sol_file_exists and args.compare:
                logger.log_msg(FileNotFoundError, f'Query file "{q_sol}" does not exist!', log.WARNING)
                
            if args.ruleset:
                # only executed when -l, --ldfu
                executed = proceed_with_ldfu(config.ldfu_path, config.ldfu_rulesets, args.ruleset,
                                queries=pair, file_str=' '.join(files), timestamp=ts, idm=idms[0], logger=logger)
                if not executed: break
                # get d    
                return d
            n = proceed_with_rdflib(g, pair, ts, idms[0], sol_file_exists, logger)
            d[os.path.split(q_req)[1]] = (n == 0) # d[query name] = True/False -> Passed or not
        return d

def init() -> Tuple[Config, Logger]:
    """initalizes current directory, configuration and logger
    """
    # ensure current working directory
    os.chdir(os.path.dirname(__file__))
    # load config file 
    config  = Config(os.getcwd(), 'config.ini')

    if config.clear_results:
        clear_folder(os.path.join(os.getcwd(), 'results'))
    # set logging configurations
    logger = Logger(os.path.join(os.getcwd(), config.logfile), config.handle_errors)
    return config,  logger #configure_log(config.logfile)

def get_args() -> argparse.Namespace:
    """set and return commandline arguments
    """
    # return query path and applied ruleset
    parser = argparse.ArgumentParser(add_help=True)
    # positional arguments
    parser.add_argument("query", help='SPARQL file in folder "requests" to be executed. "all" executes entire folder. "test" starts datatype check for RDF documents.')
    # optional arguments
    parser.add_argument("-l", "--ldfu", dest='ruleset',choices=['all', 'owl', 'rdf', 'rdfs'], help="Select 'all', 'owl', 'rdf', 'rdfs'.")
    parser.add_argument("-u", "--update", dest='update', action="store_true", help="Create resource iris in files file from Idm file")
    parser.add_argument("-c", "--compare", dest='compare', action="store_true", help='SPARQL files in folder "requests" and "solutions" are executed.')
    parser.add_argument("-s", "--single-eval", dest='single', action="store_true", help='Compares results and solutions of single idm and creates an overview file.')
    parser.add_argument("-i", "--idm", dest='idm', help='Single idm to be evaluated (independant of idm file)')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    config, logger = init()
    main(config, logger)

    if logger.compare_lines():
        print('Program finished.')
    else:
        # New log line(s) was/were added
        print('Program raised error(s). Please check the log file for more information.')