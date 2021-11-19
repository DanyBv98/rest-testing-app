from enum import Enum
from typing import Any, Dict, Optional

from Resource import Resource


class User(Resource):
    class Status(Enum):
        inactive = 0
        active   = 1
    
    class Gender(Enum):
        male   = 1
        female = 2

    def __init__(self, name : str, email : str, gender : Gender, status : Status, id : Optional[int] = None) -> None:
        super().__init__(id)

        self.name   = name
        self.email  = email
        self.gender = gender
        self.status = status

    @staticmethod
    def _from_dict(obj : Dict[str, Any]) -> 'User':
        return User(id     = obj.get('id'), 
                    name   = obj.get('name'), 
                    email  = obj.get('email'), 
                    gender = User.Gender[obj['gender']] if 'gender' in obj else None, 
                    status = User.Status[obj['status']] if 'status' in obj else None)

    def _to_data(self) -> Dict[str, Any]:
        return {
            'name'  : self.name,
            'email' : self.email,
            'gender': self.gender.name,
            'status': self.status.name
        }