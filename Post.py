from typing import Annotated, Any, Dict, List, Optional
from Comment import Comment
from Resource import Resource, ResourceRelationshipAnnotation

class Post(Resource):
    user_id : int
    title : str
    body : str

    comments : Annotated[List[Comment], ResourceRelationshipAnnotation(mapping={'post_id' : 'id'})]
    
    def __init__(self, user_id : int, title : str, body : str, id : Optional[int] = None) -> None:
        super().__init__(id)

        self.user_id = user_id
        self.title   = title
        self.body    = body

        self.comments = []

    @staticmethod
    def _from_dict(obj : Dict[str, Any]) -> 'Post':
        post = Post(id      = obj.get('id'), 
                    user_id = obj.get('user_id'), 
                    title   = obj.get('title'),
                    body    = obj.get('body'))
        Resource._children_from_dict(post, obj)
        return post

    def _to_data(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'title'  : self.title,
            'body'   : self.body,
        }
