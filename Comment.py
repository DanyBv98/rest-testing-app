from typing import Any, Dict, Optional
from Resource import Resource

class Comment(Resource):
    post_id : int
    name : str
    email : str
    body : str

    def __init__(self, post_id : int, name : str, email : str, body : str, id : Optional[int] = None) -> None:
        super().__init__(id)

        self.post_id = post_id
        self.name    = name
        self.email   = email
        self.body    = body

    @staticmethod
    def _from_dict(obj : Dict[str, Any]) -> 'Comment':
        return Comment(id      = obj.get('id'), 
                       post_id = obj.get('post_id'), 
                       name    = obj.get('name'), 
                       email   = obj.get('email'),
                       body    = obj.get('body'))

    def _to_data(self) -> Dict[str, Any]:
        return {
            'post_id': self.post_id,
            'name'   : self.name,
            'email'  : self.email,
            'body'   : self.body
        }
