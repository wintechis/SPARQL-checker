from rdflib import RDF, XSD

class DtSolutions:
    """This class contains the expected results of SPARQL queries asking for
    datatype objects. Dictionary names must be the same as the filenames containing
    the SPARQL queries. For example, the query file "me.rq" is compared with the result
    from dictionary "me".
    The keys of the dictionaries must be rdflib URIRef. By using the namespaces, spelling mistakes
    can be prevented.
    """

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
    print('Check datatypes with "python checker.py test [-s]"')