from typing import Dict
from Resource import Resource

class Comment(Resource):
    _endpoint = '/comments'

    def __init__(self, post_id : int, name : str, email : str, body : str, id : int = None) -> None:
        super().__init__(id)

        self.post_id = post_id
        self.name    = name
        self.email   = email
        self.body    = body

    @staticmethod
    def _from_dict(obj : Dict[str, object]) -> 'Comment':
        return Comment(id      = obj['id'], 
                       post_id = obj['post_id'], 
                       name    = obj['name'], 
                       email   = obj['email'],
                       body    = obj['body'])

    def _to_data(self) -> dict:
        return {
            'post_id': self.post_id,
            'name'   : self.name,
            'email'  : self.email,
            'body'   : self.body
        }
