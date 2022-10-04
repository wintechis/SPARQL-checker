
import configparser
import os

class Config:
    """This class simplifies the access to the configuration file's content.

    :param cwd: path to current directory
    :param config_file: path to config.ini
    """
    def __init__(self, cwd: str, config_file: str):
        self.cwd = cwd
        config = self.__load_config(config_file)
        self.__set_attributes(config)


    def __load_config(self, config_file: str) -> configparser.ConfigParser:    
        """returns configuration object that allows empty values for keys.

        :param config_file: path to config.ini
        :return: object containing configuration settings accessible via labels
        """

        config = configparser.ConfigParser(allow_no_value=True, interpolation=configparser.ExtendedInterpolation())
        config.read(config_file)
        return config

    def __set_attributes(self,  config: configparser.ConfigParser):
        """set instance attribues from configuration object

        :param config: configuration object
        """
        # [general]
        self.overwrite          = config['general'].getboolean('overwrite')
        self.clear_results      = config['general'].getboolean('clear_results')
        self.local_store_path   = config['general']['local_store_path']
        self.logfile            = config['general']['log_file']
        self.handle_errors      = config['general'].getboolean('handle_errors')
        
        # [data]
        self.remote_base_url    = config['data']['base_path'] 
        self.include_idms       = config['data'].getboolean('include_idms')
        self.idms_file          = os.path.join(self.cwd, config['data']['idm_list'])
        self.files_file         = os.path.join(self.cwd, config['data']['file_list'])
        
        # [files]
        self.filenames          = list(config['files'].keys())

        # [ldfu]
        self.ldfu_path          = config['ldfu']['bin_path']
        
        # [rulesets]
        self.ldfu_rulesets      = config['rulesets']

    
    def get_remote_query_url(self, idm: str, query_name: str) -> str:
        """Returns remote query url based on configuration. 
        It is expected that web resources are in folder "requests".

        :param idm: student identifier (8 chars)
        :param query_name: SPARQL query name
        :return: returns remote query url
        """
        url = self.remote_base_url[:-1] if self.remote_base_url.endswith('/') else self.remote_base_url
        return f'{url}{idm}/requests/{query_name}'

    def get_local_query_path(self, idm: str, query_name: str) -> str:
        """Returns path to local query file based on idm.
        It is expected that local queries are in folder "requests"

        :param idm: student identifier (8 chars)
        :param query_name: SPARQL query name
        :return: returns path to local query file
        """
        return os.path.join(os.getcwd(), 'requests', idm, query_name)


    








