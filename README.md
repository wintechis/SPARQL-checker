# Summary
SPARQL checker is a command tool to test and evaluate web resources and SPARQL queries. It was developed for the graduate course [Foundations of Linked Data](https://www.ti.rw.fau.de/courses/foundations-of-linked-data/) offered at the Friedrich-Alexander-Universität Erlangen-Nürnberg (FAU).
The tool provides the following features:
* Execute (online-hosted/local) SPARQL queries and save result as file.
* Compare the result of two SPARQL queries and save differences as file.
* Execute SPARQL queries with entailment rules (using [Linked Data-Fu](https://linked-data-fu.github.io/)) and save result as file.

Additional features for lecturers:
* Download online-hosted files of students and save them as proof of submission
* Compare students' SPARQL queries with solution queries and create overview file
* Evaluate students' RDF documents based on XSD datatypes and create overview file (TODO)   


# Installation
1. Clone the GitHub-Repository
```shell
git clone https://github.com/wintechis/SPARQL-checker.git checker
```

2. Go to folder "checker" and create virtual environment. Also activate venv (here: Windows)
```shell
cd checker
python -m venv env
env/scripts/activate
```
3. Install dependencies. The application uses RDFLib to handel RDF data and PrettyTable to create nice-looking text-based tables.
```shell
pip install rdflib prettytable
```
If you want to work with rule entailment, you also need the ldfu application that can be requested on the following website: https://linked-data-fu.github.io/. Unpack the ldfu folder to the current working directory that its folder "bin" is on the first-level.

Ldfu is a Java application and therefore you must have installed a Java runtime environment(https://www.java.com/de/download/). Make sure that you set Java as a global variable.

To test ldfu, adhere to the following command pattern (Windows):
```shell
ldfu.bat -q SPARQL_FILE OUTPUT_FILE -p RULESET -i RDF_FILE_1 RDF_FILE_2 ...
```

# Relevant Directories and Files
* checker.py    -> script main file
* config.ini    -> contains configuration options
* requests/     -> folder to store SPARQL queries
* solutions/    -> folder to store SPARQL queries to compare with
* results/      -> folder where all result files are saved
* rulesets/     -> folder to save entailment rulesets for ldfu


Additional standard configuration (can be changed in config.ini):
* idm.txt       -> contains a student id per line
* files.txt     -> contains the IRIs to all RDF documents the SPARQL queries will consider
* files/    -> target folder to save RDF documents locally
* error.log -> contains error messages when the program could not run properly 

The remaining files can be ignored for users.


# How to Use

## Command overview
Use the help parameter to see available execution options.
```python
python checker.py --help
```
Output:

checker.py [-h] [-l {all,owl,rdf,rdfs}] [-u] [-c] [-s] query

positional arguments:
  query                 SPARQL file in folder "requests" to be executed. "all" executes entire folder.

optional arguments:
  -h, --help            show this help message and exit
  -l {all,owl,rdf,rdfs}, --ldfu {all,owl,rdf,rdfs}
                        Select 'all', 'owl', 'rdf', 'rdfs'.
  -u, --update          Create resource iris in files file from Idm file
  -c, --compare         SPARQL files in folder "requests" and "solutions" are executed.
  -s, --single-eval     Compares results and solutions of single idm and creates an overview file.


## Positional Arguments
"query" is the only positional argument and must be the name of a query file in folder "requests". Note that the file extension of a SPARQL query is ".rq" which can be omitted. If there is a file named "query.rq", you can just write "query". If you want to execute all SPARQL queries in folder "requests", type the value "all" instead of a query name. This also means that you cannot name a SPARQL file "all.rq".

## Optional Arguments
| Arguments        | Description
|:-----------------|:----------------------------------------------------------------:|
|-u, --update      | Based on the data and files section in config.ini, IRIs are saved in file_list in the format {base_path}{idm}/{file_name}. |
|-c, --compare     | Three result files are generated: result of query in requests (req), result from query in solutions with the same query name (sol) and file containing the differences of both results (dif). If there is no solution query, sol and dif file are not created. | 
|-s, --single-eval | Files from each student ID are evaluted separately and an overview file is generated at the end. -u and -c flag are set automatically. |
|-l, --ldfu        | Execution with ldfu with one of the stated rulesets {all,owl,rdf,rdfs}. Results are saved in .tsv format.

Also have a look at possible [configurations](md/config.md).

