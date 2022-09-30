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
    print('Check datatypes with "python checker.py test [-s]"')