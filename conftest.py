import pytest

import toml

from TomlResourceParser import TomlResourceParser

from Api import Api

from User import User
from Post import Post
from Comment import Comment
from Todo import Todo

@pytest.fixture()
def api(request):
    with open('config.toml', 'r') as f:
        config = toml.load(f)

    api = Api(root = config['api']['root'], 
                access_token = config['api']['access_token'],
                endpoints={User: '/users', Post: '/posts', Comment: '/comments', Todo: '/todos'})

    def cleanup():
        api.cleanup()

    request.addfinalizer(cleanup)
    
    return api

@pytest.fixture()
def parser():
    return TomlResourceParser({
        "User"   : User,
        "Post"   : Post,
        "Todo"   : Todo,
        "Comment": Comment
    })

@pytest.fixture
def data_folder():
    return "test_data"

@pytest.fixture()
def parser_objs(data_folder, parser, test_group, test_toml):
    return parser.parse(f'{data_folder}/{test_group}/{test_toml}')

@pytest.fixture()
def users(parser_objs):
    return parser_objs[User]
@pytest.fixture()
def posts(parser_objs):
    return parser_objs[Post]
@pytest.fixture()
def comments(parser_objs):
    return parser_objs[Comment]
@pytest.fixture()
def todos(parser_objs):
    return parser_objs[Todo]
