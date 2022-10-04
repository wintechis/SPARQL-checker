# Overview of Scenarios

## For Students

### Execute single SPARQL query with fixed files list
Given the SPARQL query QUERY and a fixed files list, just execute:
```shell
python checker.py QUERY
```
Find the result set in folder "results".

### Check single SPARQL query with empty files list
Given the SPARQL query QUERY and the idm ab12cdef, you can either write your idm to the idm file or use the -idm flag. The update flag ensures that the web resources are written to the files list.
```shell
python checker.py QUERY -ui ab12cdef
```
Find the result set in folder "results".

### Execute SPARQl query wit entailment rules (using ldfu) and fixed files list
 ```shell
python checker.py QUERY -l RULESET
```

### Execute all SPARQL queries
As above, but QUERY must be "all".

## For Tutors / Lecturers

### Check RDF document datatypes
If RDF documents from students must be validated, the tool provides the feature to compare the type and amount of literals in the RDF documents.

Folder "dt_check" contains the SPARQL SELECT queries that retrieve the variables datatype and amount of datatype. It is recommended to test for the literals of single subjects in the RDF document. The expected solutions are dictionaries in "\_\_init\_\_.py" with the same name as a query file (e.g., fau -> fau.rq). Query files without a dictionary are not considered in the evaluation.

To execute the datatype check for each student, type:
```shell
python checker.py test -usc
```
The program creates in folder "results" an overview report, where for each idm all tests are described as _PASSED_ or _FAILED_. For each idm, a report is created that lists all tests with found datatype, expected datatypes and difference.

_Remark: The program checks the lexical form of datatypes (e.g., xsd:int and xsd:integer are not the same)._


## Check SPARQL queries on fixed RDF documents
If SPARQL queries from students must be validated, the tool provides the feature to compare the result sets from a student's query and the lectuter's query in folder "solutions" with the same name.

Each student query must be saved in directory "requests/(student idm)/(query)". Query files can be downloaded from the Web following the data configurations "(base_path)(idm)/requests/(query).

To execute the SPARQL comparison, type:
```shell
python checker.py QUERY -sc
```
QUERY is the name of the query file (with or without the file extension _.rq_). If QUERY is ALL, all solution queries with available student queries are executed.

The program creates in folder "results" files containing the result set of the student's query, the solution query and a file containing the differences. Also an overview report, where for each idm all query test comparisons are described as _PASSED_ or _FAILED_, is generated.

_Remark_: The solution file is created for each idm, if the update flag is set.

## Check SPARQL queries on idm-specific RDF documents
As above, but with the update flag.
```shell
python checker.py QUERY -usc
```

## Check SPARQL queries for fixed RDF documents with entailment rules.
If SPARQL queries from students must be validated using entailment patterns, the tool provides the feature to compare the result sets from a student's query and the lectuter's query in folder "solutions" with the same name using [Linked Data-Fu](https://linked-data-fu.github.io/).

To execute the SPARQL comparison, type:
```shell
python checker.py QUERY -scl RULESET
```
RULESET must be the name of the entailment file in folder "RULESETS".
Ldfu creates tsv files as result.

## Check SPARQL queries for idm-specific RDF documents with entailment rules.
As above, but with the update flag.
```shell
python checker.py QUERY -uscl RULESET
```