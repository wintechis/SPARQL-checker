from datetime import date
from email import header
import os

from typing import  Iterator, Tuple, Dict, List, Union
from zipfile import ZipFile
from rdflib import Graph
from rdflib.query import Result, ResultRow
from pyparsing.exceptions import ParseException
from check_task1 import evaluate_task1
import urllib.request
from prettytable import PrettyTable

URL = 'https ...'

def print_progress(completed: int, all: int) -> None:
    progress = int(completed/all*100)
    end='\n' if progress == 100 else ''
    print('\u2588'*progress + '\u2581'*(100 - progress) + f' {progress}%\r', end=end)

def main():
    main_folder = 'Task2_submissions'
    rst_file = 'task2_results.csv'
    rq_solutions = get_solutions('requests_2')
    tbl = PrettyTable(header=True)

    lst_tbl = []
    all = i = 0

    for root, dirs, files in os.walk(main_folder):
        for i, file in enumerate(files):
            if file.endswith('.zip'):
                all+= 1

    for root, dirs, files in os.walk(main_folder):
        for file in files:
            if file.endswith('.zip'):
                i+= 1
                tpl_student = get_student_data(os.path.basename(root))
                paul_uri = URL + tpl_student[1] + '/fld.ttl'
                save_fld_file(paul_uri, tpl_student[2], tpl_student[1])
                rq_student = get_sparql_queries(os.path.join(root, file), rq_solutions.keys())
                dct_results = run_comparison(rq_student, rq_solutions, paul_uri)
                dct_results_task1 = evaluate_task1(f'{URL}{tpl_student[1]}/fld.ttl')
                lst_tbl.append(add_row(tpl_student, dct_results, dct_results_task1))
            print_progress(i, all)
    
    lst_tbl.sort(key=lambda l: l[0])
    for i,l in enumerate(lst_tbl, start=1):
        l.insert(0, i)
        tbl.add_row(l)
   
    tbl.field_names = ['#', *add_row(('NAME', 'IDM', 'MATR.NO'), {k:k for k in  rq_solutions.keys()},\
        {'subjects': 'subjects', 'dt_me':'dt_me', 'dt_fau':'dt_fau', 'dt_thesis':'dt_thesis'})]
    write_to_file(rst_file, tbl.get_string())

def add_row(student: Tuple[str], task2: Dict[str, str], task1: Dict[str, bool]) -> List[str]:
    #s = f'{student[2]}, {student[1]}, {student[0]}, '
    all = []
    for k in sorted(task1.keys()):
        all.append(task1[k])
        #s += f'{task1[k]}, '
    for k in sorted(task2.keys()):
        all.append(task2[k])
        #s += f'{task2[k]}, '

    
    all.insert(0, f'{all.count(True)}/{len(all)}, ' if student[0] !='NAME' else 'PASSED')
    #s += ','.join(map(str,all))
    return [student[1], *all]
    

def write_to_file(filename: str, s: str) -> None:
    with open(filename, 'w') as f:
        f.write(s)


def run_comparison(queries: Dict[str,str], solutions: Dict[str,str], uri: str) -> Dict[str, str]:
    d = {k:'not run!' for k in solutions.keys()}
    try:
        g = Graph().parse(uri)
        for rq in queries.keys():
            #if not rq == 'construct.rq': continue
            try:
                a = g.query(queries[rq])
                b = g.query(solutions[rq])
                d[rq] = compare_results(a,b)
            except ParseException as e:
                d[rq] = 'ParseException'
    except Exception as e:
        d['abstract.rq'] = 'Bad Syntax'
    return d

def compare_results(rst_student: Result, rst_solution: Result) -> str:
    lst_student = convert_row_to_lst(rst_student)
    lst_solution = convert_row_to_lst(rst_solution)
    matches = 0
    if len(lst_solution) != len(lst_student): return f'Expected {len(lst_solution)}, but {len(lst_student)}'
    try:
        for s in lst_solution:
            for s_2 in lst_student:
                if s == s_2:
                    matches += 1
                    #lst_solution.remove(s)
                    #lst_student.remove(s_2)
                    continue
        
        if len(lst_solution) == matches:
            rst = True
        else:
            rst = f'MatchDiff: {len(lst_solution) - matches}'
    except Exception as e:
       rst = 'Bad Syntax'
    return rst

def convert_row_to_lst(rst: Result) -> List[List[Union[str, int, float, date]]]:
    l = []
    if rst.type == 'ASK': return [rst.askAnswer]
    for row in rst:
        if isinstance(row,Tuple): 
            l.append('_'.join(sorted(map(str,[val.toPython() for val in row]))))
            continue
        l.append('_'.join(sorted(map(str,[val.toPython() for val in row.asdict().values()]))))
    return l
    


def get_solutions(rq_folder: str) -> Dict[str, str]:
    d = dict()
    for root, dirs, files in os.walk(rq_folder):
        for file in files:
            if file.endswith('.rq'):
                with open(os.path.join(root, file), 'r') as f:
                    d[file] = f.read()
    return d

def get_sparql_queries(zip_path: str, rq_names: Iterator[str]) -> Dict[str, str]:
    d = dict()
    for rq in rq_names:
        with ZipFile(zip_path, 'r') as zip:
            for name in zip.namelist():
                if name.endswith(rq) and name.find('MACOSX') < 0:
                    d[rq] = zip.read(name)
    return d

def get_student_data(base_name: str) -> Tuple[str]:
    # [0] matr.nr [1] idm [2] name
    lst = base_name.split('_')
    return (lst.pop(), lst.pop(), ' '.join(map(str,lst)))


def save_fld_file(path: str,name:str, idm: str) -> None:
    try:
        urllib.request.urlretrieve(path, f"fld/{name}_{idm}.ttl")
    except urllib.error.HTTPError:
        pass
if __name__ == '__main__':
    main()