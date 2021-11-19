from enum import Enum
from typing import Dict

from Resource import Resource


class User(Resource):
    class Status(Enum):
        inactive = 0
        active   = 1
    
    class Gender(Enum):
        male   = 1
        female = 2

    def __init__(self, name : str, email : str, gender : Gender, status : Status, id = None) -> None:
        super().__init__(id)

        self.name   = name
        self.email  = email
        self.gender = gender
        self.status = status

    @staticmethod
    def _from_dict(obj : Dict[str, object]) -> 'User':
        return User(id     = obj['id'], 
                    name   = obj['name'], 
                    email  = obj['email'], 
                    gender = User.Gender[obj['gender']], 
                    status = User.Status[obj['status']])

    def _to_data(self) -> dict:
        return {
            'name'  : self.name,
            'email' : self.email,
            'gender': self.gender.name,
            'status': self.status.name
        }