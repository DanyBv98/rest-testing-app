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
    def __init__(self, resource_types : Dict[str, Type]) -> None:
        self.__resource_types = resource_types
    
    def parse(self, file_path : str) -> List[Resource]:
        with open(file_path, 'r', encoding='utf-8') as f:
            toml_dict = toml.load(f)

        if '_metadata' not in toml_dict or 'resources' not in toml_dict['_metadata']:
            raise TomlResourceParserInvalidFileError('A TOML resource file should contain metadata for the contained resources.')
        
        metadata = toml_dict['_metadata']['resources']
        for resource_name in metadata.values():
            if resource_name not in self.__resource_types:
                raise TomlResourceParserTypeNotFoundError(resource_name)

        resources : dict[Type, List[Resource]] = {}

        data = toml_dict['data']
        for d in data:
            if d in metadata:
                resource_type = self.__resource_types[metadata[d]]
                if resource_type not in resources:
                    resources[resource_type] = []
                resources[resource_type].extend([resource_type._from_dict(r) for r in data[d].values()])
        
        return resources
