from typing import Tuple, Dict, Any
import rdflib


def convert_rst_to_dict(rst: rdflib.query.Result) -> Dict[str,Any]:
    d = {'header': 'ASK QUERY',
         'type': rst.type,
         'list'  : []}
    l = d['list']
    if rst.type == 'ASK':
        l.append(rst.askAnswer)
        return d
    elif rst.type == 'CONSTRUCT':
         d['list'] = rst.serialize(format='ttl').decode(('utf-8'))
         return d
    elif rst.type == 'SELECT':
        d['header'] = [var.toPython() for var in rst.vars]

    for row in rst:
        if isinstance(row,Tuple): # CONSTRUCT
            l.append('\u2312'.join(sorted(map(str,[val.toPython() for val in row]))))
            continue
        #SELECT
        l.append('\u2312'.join(sorted(map(str,[val.toPython() for val in row.asdict().values()]))))
    return d


