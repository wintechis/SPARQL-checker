from genericpath import isfile
import os
import platform
from subprocess import Popen, PIPE
import logging as log
from typing import Dict, List, Tuple

from etc import get_target_file
from file_handling import (get_file_lines,
                           save_file
                          )
        

def proceed_with_ldfu(config_ldfu: Dict[str,str], config_ruleset: Dict[str,str], active_ruleset: str,
                      queries: List[str], file_str: str, timestamp: str, idm: str) -> bool:
    script_path  = get_script_path(config_ldfu)
    ruleset = get_ruleset(config_ruleset, active_ruleset)

    if  not (is_java_installed and ldfu_script_exists(script_path) and ruleset_exists(ruleset)):
        # check, if ldfu can run properly
        return False

    target_files = execute_ldfu(script_path, ruleset, file_str=file_str, 
                                    queries=queries, timestamp=timestamp, idm=idm)
    if len(target_files) == 2: 
        create_diff(queries[0], timestamp, idm, *target_files)
    elif len(target_files) != len(queries): 
        log.error(f'Ldfu could not process SPARQL query. Check terminal output! ({" ,".join(queries)})')
    return True
            
def execute_ldfu(script_path: str, ruleset: str, file_str:str,
                 queries:List[str],  timestamp: str, idm: str) -> List[str]:
    
    target_files = []
    for i, q in enumerate(queries):
        if os.path.isfile(q):
            out = get_target_file(q, ('req', 'sol')[i], timestamp, idm)
            run_ldfu_script(script_path, query=q, target_file=out, ruleset=ruleset, files=file_str)
            target_files.append(out)
    return target_files

def get_ruleset(rulesets: Dict[str, str], ruleset: str) -> str:
    return os.path.join(os.getcwd(), 
                        rulesets['path'], 
                        rulesets[ruleset]
                        )

def get_script_path(ldfu_config: Dict[str, str]):
    script = 'ldfu.bat' if platform.system() == 'Windows' else 'ldfu.sh'
    return os.path.join(os.getcwd(),
                          ldfu_config['bin_path'],
                          script
                        )
                    
def run_ldfu_script(script: str, query:str, target_file:str, ruleset: str, files: str) -> None:
    # invoke ldfu script with parameters
    p = Popen(f'{script} -q {query} "{target_file}"  -p {ruleset} -i {files}', shell=True, stdout=PIPE, cwd=os.getcwd())
    p.communicate()

def create_diff(query: str, ts: str, idm, res: str, sol: str) -> int:
    target_file = get_target_file(query, 'dif', ts, idm)
    a, b = get_file_lines(res), get_file_lines(sol)
    content, n = get_diff_tsv(a,b)
    save_file(target_file, content)
    return n

def get_diff_tsv(one: List[str], other: List[str]) -> Tuple[str, int]:
    diff_extra = [f'+:\t{line}' for line in one if line not in other]
    diff_miss = [f'-:\t{line}' for line in other if line not in one]
    content = '\n'.join([one[0], *diff_extra, '\n', *diff_miss])
    n = len(diff_extra) + len(diff_miss)
    return (content, n)

def is_java_installed() -> bool:
    if ('java' in os.environ.get('PATH',default='')):
        return True
    log.error('Java is not registered as PATH environ variable and is required to execute ldfu.')
    return False

def ldfu_script_exists(script_path: str) -> bool:
    if os.path.isfile(script_path):
        return True
    log.error(f'Ldfu script could not be found at path "{script_path}".')
    return False

def ruleset_exists(ruleset_path:str) -> bool:
    if os.path.isfile(ruleset_path):
        return True
    log.error(f'Ruleset file could not be found at path "{ruleset_path}".')
    return False