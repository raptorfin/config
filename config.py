import yaml

class ConfigRuleset(dict):
    defaults = {}
    required = []
    
    def __init__(self):
        self.update(self.defaults)

    def validate(self):
        missing = [k for k in self.required if k not in self]
        if missing:
            raise KeyError("Missing the following keys: {}".format(missing))


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
            pass
        return data


class YAMLConfigProvider(FileConfigProvider):
    def __init__(self, src="config.yaml"):
        FileConfigProvider.__init__(self, src)

    def load_config(self):
        entries = yaml.load(self.load_file_data())
        if entries:
            self.update(entries)


if __name__ == '__main__':
    y = YAMLConfigProvider()
    y.required = ['name', 'sex']
    y.validate()
    