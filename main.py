from typing import Dict, List
import random

from Resource import Resource
from TomlResourceParser import TomlResourceParser

from User import User
from Post import Post
from Todo import Todo
from Comment import Comment

from Api import Api

import toml

def fill_orphans(orphans : List[Resource], parents : List[Resource], fill_map : Dict[str, str]):
    for orphan in orphans:
        parent = random.choice(parents)
        for property in fill_map:
            if not getattr(orphan, property):
                setattr(orphan, property, getattr(parent, fill_map[property]))

if __name__ == "__main__":
    parser = TomlResourceParser({
        "User"   : User,
        "Post"   : Post,
        "Todo"   : Todo,
        "Comment": Comment
    })

    users    = parser.parse('data/users.toml'   )
    posts    = parser.parse('data/posts.toml'   )
    todos    = parser.parse('data/todos.toml'   )
    comments = parser.parse('data/comments.toml')
    
    with open('config.toml', 'r') as f:
        config = toml.load(f)

    api = Api(root = config['api']['root'], 
              access_token = config['api']['access_token'],
              endpoints={User: '/users', Post: '/posts', Comment: '/comments', Todo: '/todos'})

    for u in users:
        api.create(u)
        print(u._to_data())
        
    fill_orphans(posts, users, {'user_id': 'id'})
    for p in posts:
        api.create(p)
        print(p._to_data())

    fill_orphans(comments, posts, {'post_id': 'id'})
    fill_orphans(comments, users, {'name': 'name', 'email': 'email'})
    for c in comments:
        api.create(c)
        print(c._to_data())

    fill_orphans(todos, users, {'user_id': 'id'})
    for t in todos:
        api.create(t)
        print(t._to_data())

    api.cleanup()
