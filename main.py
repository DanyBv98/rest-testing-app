from datetime import datetime, timedelta, timezone
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

    todo = Todo(user.id, 'Testing', datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(hours = 2), Todo.Status.pending)
    api.create(todo)
    print(todo.due_on)
    todo = api.fetch(Todo, todo.id)
    print(todo.due_on)
    api.delete(todo)

    print(user.id)
    api.cleanup()
    print(user.id)