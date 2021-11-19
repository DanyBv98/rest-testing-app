from typing import Any, Dict, Optional
from Resource import Resource

class Comment(Resource):
    def __init__(self, post_id : int, name : str, email : str, body : str, id : Optional[int] = None) -> None:
        super().__init__(id)

        self.post_id = post_id
        self.name    = name
        self.email   = email
        self.body    = body

    @staticmethod
    def _from_dict(obj : Dict[str, Any]) -> 'Comment':
        return Comment(id      = obj['id'], 
                       post_id = obj['post_id'], 
                       name    = obj['name'], 
                       email   = obj['email'],
                       body    = obj['body'])

    def _to_data(self) -> Dict[str, Any]:
        return {
            'post_id': self.post_id,
            'name'   : self.name,
            'email'  : self.email,
            'body'   : self.body
        }
