import json
import yaml
from yaml import Loader, Dumper

class DICTIONARY(dict):
    def __init__(self, **response):
        for k,v in response.items():
            if isinstance(v, dict):
                self.__dict__[k] = DICTIONARY(**v)
            else:
                self.__dict__[k] = v
                
        super(DICTIONARY, self).__init__(self.__dict__)
                                
    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)
        
    def __len__(self):
        return len(self.__dict__)
    
    def keys(self):
        return list(self.__dict__.keys())
    
    def to_yaml(self):
        yaml_dict = {}
        for k, v in self.__dict__.items():
            if isinstance(v, DICTIONARY):
                v = v.to_yaml()
            yaml_dict[k] = v
        return yaml_dict


class CONFIG(DICTIONARY):
    def __init__(self, config_file='./base_config.yaml', **kwargs):

        with open(config_file) as f:
            config = yaml.load(f, Loader=Loader)

        for key, val in kwargs.items():
            config[key] = val

        super(CONFIG, self).__init__(**config)
        
    def save(self, path):
        if path.endswith('\r.*'):
            with open(path, 'w') as f:
                yaml_obj = self.to_yaml()
                Dumper.ignore_aliases = lambda *args : True
                yaml.dump(yaml_obj, f, Dumper=Dumper)