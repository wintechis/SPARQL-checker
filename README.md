# TODO: this refers still to the old application

# Remark: assume the current working directory "../ldfu/." in Windows.

This README explains how to use the Python wrapper to work with ldfu.
ldfu does not support Turtle1.1 syntax with PREFIX. The wrapper retrieves remote resources and saves them locally after replacing @prefix with PREFIX. If you have used only @prefix, you can use ldfu directly with:

´´´shell
bin/ldfu.bat -q SPARQL_FILE RESULT_FILE -p RULESET -i FILE FILE [...]
´´´


# Installation
1. Install java (https://www.java.com/en/download/help/download_options.html)
2. Make sure to have java as a global

3. Install python env. Open terminal, eg. PowerShell and type
´´´shell
python -m venv env
´´´
# Preparation
* Activate virtal environment
´´´shell
env/scripts/activate
´´´

# Directories and files
* requests/ -> Folder to store SPARQL queries
* results/ -> Folder where result is saved as query_rst_timestamp.tsv
* files/ -> local files with @prefix syntax
* files.txt -> one URL per line
* idm.txt -> one idm per line
* ldfu.py -> Python wrapper for ldfu
* ignore the rest


# Use
´´´shell
python ldfu.py SPARQL_QUERY -r RULESET
´´´
SPARQL_QUERY - if you saved your query in "requests", you can just write the name,e.g. test.rq
RULESET - choose all, owl, rdfs, or rdf. Default is all

The result is saved in folder results.
Included are all files in folder "files".

You can use files.txt to store a list of remote resources that shall be locally saved.

If you are lazy, you can also use idm.txt and the following command to create files.txt:
´´´shell
python ldfu.py SPARQL_QUERY -r RULESET --idm
´´´

# Remark: As you can see in config.py, you should have a file named mapping.ttl and fld.ttl. So make sure they are available on Paul. 


Application Example:
1. Open idm.txt and insert my idm xy55peqe
2. Execute "python ldfu.py test.rq -r rdfs --idm"
3. Check result:
You should see the three people I know. Thanks to rdfs-entailment we could derive :name -> foaf:name

4. Execute "python ldfu.py test.rq -r owl"
5. Check result:
Beside my URIs of the three, there are also the three URI of the FAU namespace thanks to owl-entailment.

If you feel like it, you can create SPARQL queries that also include information of students you have mentioned as someone you know to close the gap of locally data.
