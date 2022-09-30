# Information for Tutors / Lecturers


## USE CASE A: Students create RDF documents
If RDF documents from students must be validated, the tool provides the feature to compare the type and amount of literals in the RDF documents.

Folder "dt_check" contains the SPARQL SELECT queries that retrieve the variables datatype and amount of datatype. It is recommended to test for the literals of single subjects in the RDF document. The expected solutions are dictionaries in "\_\_init\_\_.py" with the same name as a query file (e.g., fau -> fau.rq). Query files without a dictionary are not considered in the evaluation.

To execute the datatype check, type:
```shell
python checker.py test [-i IDM] [-s --single-eval]
```
The program creates in folder "results" an overview report, where for each idm all tests are described as _PASSED_ or _FAILED_. For each idm, a report is created that lists all tests with found datatype, expected datatypes and difference.

_Remark: The program checks the lexical form of datatypes (e.g., xsd:int and xsd:integer are not the same)._


## USE CASE B: Students write SPARQL queries for (idm-related) RDF documents
If SPARQL queries from students must be validated, the tool provides the feature to compare the result sets from a student's query and the lectuter's query in folder "solutions" with the same name.

Each student query must be saved in directory "requests/(student idm)/(query)". Query files can be downloaded from the Web following the data configurations "(base_path)(idm)/requests/(query).

To execute the SPARQL comparison, type:
```shell
python checker.py QUERY [-i IDM] [-u --update] [-c --compare] [-s --single-eval]
```
QUERY is the name of the query file (with or without the file extension _.rq_). If QUERY is ALL, all solution queries with available student queries are executed.

The program creates in folder "results" files containing the result set of the student's query, the solution query and a file containing the differences. Also an overview report, where for each idm all query test comparisons are described as _PASSED_ or _FAILED_, is generated.

_Remark_: The solution file is created for each idm, if the update flag is set.


## USE CASE C: Students write SPARQL queries for (idm-related) RDF documents with entailment rules.
If SPARQL queries from students must be validated using entailment patterns, the tool provides the feature to compare the result sets from a student's query and the lectuter's query in folder "solutions" with the same name using [Linked Data-Fu](https://linked-data-fu.github.io/).

To execute the SPARQL comparison, type:
```shell
python checker.py QUERY [-i IDM] [-u --update] [-c --compare] [-s --single-eval] [-l --ldfu RULESET]
```
RULESET must be the name of the entailment file in folder "RULESETS".

In opposite to USE CASE B, ldfu creates tsv files as result.
