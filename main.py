import toml

from Api import Api
from Comment import Comment
from Todo import Todo

from User import User
from Post import Post

if __name__ == '__main__':
    with open('config.toml', 'r') as f:
        config = toml.load(f)

    api = Api(root = config['api']['root'], 
              access_token = config['api']['access_token'],
              endpoints={User: '/users', Post: '/posts'})

    api.add_resource(Comment, '/comments')
    api.add_resource(Todo, '/todos')

    users = api.fetch(User)

    todos = api.fetch(Todo)
    comments = api.fetch(Comment)

    user = User('Test test', 'testingro@test.com', User.Gender.male, User.Status.active)
    api.create(user)

    post = Post(user.id, 'Test post', 'Lorem ipsum')
    api.create(post)

    print(post.id)
    api.delete(post)
    print(post.id)

    print(user.id)
    api.cleanup()
    print(user.id)
