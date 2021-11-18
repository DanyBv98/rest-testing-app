from typing import List, Type
import toml

from Api import Api

from User import Gender, Status, User
from Post import Post


with open('config.toml', 'r') as f:
    config = toml.load(f)

api = Api(config['api']['root'], [User, Post], 
        access_token = config['api']['access_token'])

results = api.fetch()

user = User('Test test', 'testing1s2w2s@test.com', Gender.male, Status.active)
api.create(user)

print(user.id)

api.delete(user)
print(user.id)

api.delete(user)