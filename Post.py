from typing import Dict
from Resource import Resource

class Post(Resource):
    def __init__(self, user_id : int, title : str, body : str, id : int = None) -> None:
        super().__init__(id)

        self.user_id = user_id
        self.title   = title
        self.body    = body

    @staticmethod
    def _from_dict(obj : Dict[str, object]) -> 'Post':
        return Post(id      = obj['id'], 
                    user_id = obj['user_id'], 
                    title   = obj['title'],
                    body    = obj['body'])

    def _to_data(self) -> dict:
        return {
            'user_id': self.user_id,
            'title'  : self.title,
            'body'   : self.body,
        }
