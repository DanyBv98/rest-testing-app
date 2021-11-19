from typing import Any, Dict, Optional
from Resource import Resource

class Post(Resource):
    def __init__(self, user_id : int, title : str, body : str, id : Optional[int] = None) -> None:
        super().__init__(id)

        self.user_id = user_id
        self.title   = title
        self.body    = body

    @staticmethod
    def _from_dict(obj : Dict[str, Any]) -> 'Post':
        return Post(id      = obj.get('id'), 
                    user_id = obj.get('user_id'), 
                    title   = obj.get('title'),
                    body    = obj.get('body'))

    def _to_data(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'title'  : self.title,
            'body'   : self.body,
        }
