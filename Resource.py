from typing import Annotated, Any, Dict, Optional, Type
from dataclasses import dataclass
import typing

@dataclass(frozen=True)
class ResourceRelationshipMetadata:
    member_name : str
    resource_type : Type
    mapping : Dict[str, str]
    is_child : bool
    is_many : bool

class ResourceRelationshipAnnotation:
    def __init__(self, *, mapping : Dict[str, str] = {}, is_child : bool = True) -> None:
        self.__mapping  = mapping
        self.__is_child = is_child

    @property
    def mapping(self) -> Dict[str, str]:
        return self.__mapping

    @property
    def is_child(self) -> bool:
        return self.__is_child

class Resource:
    def __init__(self, id : Optional[int]) -> None:
        self.id = id
    
    @staticmethod
    def _from_dict(obj : Dict[str, Any]) -> 'Resource':
        return Resource(id = obj['id']) 

    def _to_data(self) -> Dict[str, Any]:
        return {'id' : self.id}

    def _get_resource_metadatas(resource : Type | 'Resource') -> Dict[str, ResourceRelationshipMetadata]:
        metadatas : Dict[str, ResourceRelationshipMetadata] = {}
        for (member, type_hint) in typing.get_type_hints(resource, include_extras=True).items():
            if typing.get_origin(type_hint) == Annotated:
                type_args = typing.get_args(type_hint)
                
                metadata_annotation = None
                for arg in type_args[1:]:
                    if isinstance(arg, ResourceRelationshipAnnotation):
                        metadata_annotation = arg
                        break

                if metadata_annotation:
                    is_many = typing.get_origin(type_args[0]) == list
                    child_type = type_args[0] if not is_many else typing.get_args(type_args[0])[0]

                    metadatas[member] = ResourceRelationshipMetadata(member, child_type, metadata_annotation.mapping, metadata_annotation.is_child, is_many)
        return metadatas
    
    def _children_from_dict(resource : 'Resource', obj : Dict[str, Any]) -> None:
        metadatas : Dict[str, ResourceRelationshipMetadata] = resource._get_resource_metadatas()
        for (member, metadata) in metadatas.items():
            if member in obj:
                data = obj[member]
                if isinstance(obj[member], dict):
                    resources = [metadata.resource_type._from_dict(resource_obj) for (name, resource_obj) in obj[member].items()]
                    setattr(resource, member, resources)