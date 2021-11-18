from typing import Dict


class Resource:
    _endpoint = None

    def __init__(self, id : int) -> None:
        self.id = id
    
    @staticmethod
    def _from_dict(obj : Dict[str, object]) -> 'Resource':
        return Resource(id = obj['id']) 

    def _to_data(self) -> dict:
        return {'id' : self.id}
