from typing import Dict, List, Type
from Resource import Resource
import toml

class TomlResourceParserError(Exception):
    def __init__(self, message : str) -> None:
        self.message = message
        super().__init__(self.message)

class TomlResourceParserInvalidFileError(Exception):
    def __init__(self, message : str) -> None:
        self.message = message
        super().__init__(self.message)

class TomlResourceParserTypeNotFoundError(TomlResourceParserError):
    def __init__(self, resource_name : str) -> None:
        super().__init__(f'The "{resource_name}" resource was not added to the current parser.')

class TomlResourceParser:
    def __init__(self, resources : Dict[str, Type]) -> None:
        self.resources = resources
    
    def parse(self, file_path : str) -> List[Resource]:
        with open(file_path, 'r', encoding='utf-8') as f:
            toml_dict = toml.load(f)

        if 'resource' not in toml_dict:
            raise TomlResourceParserInvalidFileError('A TOML resource file should contain the "resource" property.')
        
        resource_name = toml_dict['resource']
        if resource_name not in self.resources:
            raise TomlResourceParserTypeNotFoundError(resource_name)
        
        resource_type = self.resources[resource_name]
        return [resource_type._from_dict(d) for d in toml_dict['data']]
