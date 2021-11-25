from Api import Api
from TomlResourceParser import TomlResourceParser

from Comment import Comment
from Post import Post
from Todo import Todo
from User import User

import toml
import traceback

if __name__ == '__main__':
    parser = TomlResourceParser({
        "User"   : User,
        "Post"   : Post,
        "Todo"   : Todo,
        "Comment": Comment
    })

    resources = parser.parse('data/nested.toml')

    with open('config.toml', 'r') as f:
        config = toml.load(f)

    api = Api(root = config['api']['root'], 
                access_token = config['api']['access_token'],
                endpoints={User: '/users', Post: '/posts', Comment: '/comments', Todo: '/todos'})

    try:
        for r_type in resources:
            for r in resources[r_type]:
                api.create(r, create_children=True, 
                callback=lambda r, success: print(f'{type(r).__name__} > {r.id} > {success}'))
    except:
        traceback.print_exc()
    finally:
        print("Cleaning up...")
        api.cleanup()
