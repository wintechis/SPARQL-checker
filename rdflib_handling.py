from typing import Tuple, Dict, Any, List
import rdflib


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
        if isinstance(row,Tuple): # CONSTRUCT
            l.append(f'{delim}'.join(sorted(map(str,[val.toPython() for val in row]))))
            continue
        #SELECT
        l.append(f'{delim}'.join(sorted(map(str,[val.toPython() for val in row.asdict().values()]))))
    return d


def create_lst_from_construct(rst: rdflib.query.Result, delim: str) -> List[str]:
    # 
    return [f'{delim}'.join((s.toPython(), p.toPython(), o.toPython())) for (s, p, o) in rst]

#def compare_construct_rst(one: str, other: str, sign: str, delimiter: str) -> List[str]:
#    a, b = rdflib.Graph().parse(data=one), rdflib.Graph().parse(data=other)
#    a -= b
#    l = []
#    for triple in a:
#        l.append(f'{sign}{delimiter}' + f'{delimiter}'.join(triple))
#
#    return l