"""
Configuration class which provides validation various types of configfiles.
Caller can specify both default values as well as required values.
Provides a base implementation for file formats
"""

import yaml
import logging

LOGGER = logging.getLogger(__name__)

class ConfigRuleset(dict):
    defaults = {}
    required = []

    def __init__(self):
        self.update(self.defaults)

    def validate(self):
        missing = [k for k in self.required if k not in self]
        if missing:
            keyerr = "Missing the following keys: {}".format(missing)
            logging.critical(keyerr)
            raise KeyError(keyerr)

    def update_values(self, vals):
        return self.update(vals)


class FileConfigProvider(ConfigRuleset):
    def __init__(self, src=None):
        ConfigRuleset.__init__(self)
        self.source = src
        self.load_config()

    def load_config(self):
        pass

    def load_file_data(self):
        data = ""
        try:
            with open(self.source) as f:
                data = f.read()
        except IOError as err:
            logging.critical("Unable to read file: %s", err)
        return data


class YAMLConfigProvider(FileConfigProvider):
    """
    YAML implementation of the FileConfigProvider.
    Assumes a local yaml file called config.yaml
    """
    def __init__(self, src="config.yaml"):
        FileConfigProvider.__init__(self, src)

    def load_config(self):
        entries = yaml.load(self.load_file_data())
        if entries:
            self.update(entries)


if __name__ == '__main__':
    y = YAMLConfigProvider()
    y.required.append('type')
    y.validate()
    print(y)
    
