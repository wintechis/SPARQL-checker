from rdflib import RDF, XSD

class DtSolutions:
    # Note: rdflib Namespace Variables are of type URIRef and must be converted to str
    me = {
        XSD.string:     2   ,
        XSD.integer:    1   ,
    }

    fau = {
        XSD.integer:    1   ,
        RDF.langString: 1   ,
    }

    thesis = {
        XSD.string:     1   ,
        XSD.dateTime:   1   ,
        RDF.langString: 2   ,
    }




if __name__ == "__main__":
    pass
    # expected_tests = list(get_dt_solutions().keys())
    # available_tests = get_dt_dct_tests.keys()
    # diff = set(expected_tests).difference(set(available_tests))
    # print(f'Current selected tests: {", ".join(expected_tests)}.')
    # if len(diff):
    #     print(f'The following queries are missing: {" ,".join(diff)}.')