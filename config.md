## Configurations
The config.ini contains settings to reduce the length the script command. It contains the following sections:
* general   -> general configurations
* data      -> settings for creating IRIs
* files     -> list of all considered file names
* ldfu      -> settings for ldfu
* rulesets  -> configuration for rulesets

### [general]
* overwrite         -> if "yes", existing local files are replaced with current web resource. If "no", current web resource is ignored and local file will be used.
* local_store_path  -> name of folder where files will be locally stored. If no name is given, web resources are not locally stored.
* log_file          -> name of log file
  
### [data]
base_path           -> base url (e.g. http://www.example.org/)
include_idms        -> given the idm (student id) xoxoxoxo and "yes", the new base would be http://www.example.org/xoxoxoxo/. If "no", the base url remains the same.
idm_list            -> name of file containing list of idms
file_list           -> name of file containing list of IRIs

### [files]
This section just contains all filenames as keys. Given the example in [data] and a key "doc.ttl", one IRI in file_list would be http://www.example.org/xoxoxoxo/doc.ttl.

### [ldfu]
bin_path -> directory to ldfu scripts ldfu.bat and ldfu.sh.

### [rulesets]
path -> directory to rulesets folder
All the other values map the command parameter to a ruleset file.