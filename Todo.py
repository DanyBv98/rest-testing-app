from enum import Enum
from typing import Any, Dict, Optional
from datetime import datetime

from Resource import Resource

class Todo(Resource):
    class Status(Enum):
        pending   = 0
        completed = 1

    user_id : int
    title : str
    due_on : datetime
    status : Status

    def __init__(self, user_id : int, title : str, due_on : datetime,  status : Status, id : Optional[int] = None) -> None:
        super().__init__(id)

        self.user_id = user_id
        self.title   = title
        self.due_on  = due_on
        self.status  = status

    @staticmethod
    def _from_dict(obj : Dict[str, Any]) -> 'Todo':
        return Todo(id      = obj.get('id'), 
                    user_id = obj.get('user_id'), 
                    title   = obj.get('title'),
                    due_on  = Todo.__convert_datetime(obj['due_on']) if 'due_on' in obj else None,
                    status  = Todo.Status[obj['status']] if 'status' in obj else None)

    def _to_data(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'title'  : self.title,
            'due_on' : self.due_on.isoformat(timespec='milliseconds'),
            'status' : self.status.name
        }

    @staticmethod
    def __convert_datetime(dtime : datetime | str) -> datetime:
        if isinstance(dtime, datetime): 
            return dtime
        return datetime.fromisoformat(dtime)