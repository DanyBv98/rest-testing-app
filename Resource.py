from typing import Any, Dict, Optional


class Resource:
    def __init__(self, id : Optional[int]) -> None:
        self.id = id
    
    @staticmethod
    def _from_dict(obj : Dict[str, Any]) -> 'Resource':
        return Resource(id = obj['id']) 

    def _to_data(self) -> Dict[str, Any]:
        return {'id' : self.id}
