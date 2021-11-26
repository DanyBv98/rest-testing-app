import pytest

from User import User
from Post import Post
from Comment import Comment
from Todo import Todo

class TestAdding:
    def __assert_creation(resource_type, resource, success):
        if type(resource) == resource_type:
            assert success
            assert resource.id != None

    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/valid', 'user_creation.toml')
    ])
    def test_user_add(self, api, users):
        for user in users:
            success = api.create(user)
            TestAdding.__assert_creation(User, user, success)
    
    
    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/valid', 'post_creation.toml')
    ])
    def test_post_add(self, api, users):
        for user in users:
            api.create(user, callback=lambda resource, success: 
                TestAdding.__assert_creation(Post, resource, success))
    

    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/valid', 'comment_creation.toml')
    ])
    def test_comment_add(self, api, users):
        for user in users:
            api.create(user, callback=lambda resource, success: 
                TestAdding.__assert_creation(Comment, resource, success))

    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/valid', 'todo_creation.toml')
    ])
    def test_todo_add(self, api, users):
        for user in users:
            api.create(user, callback=lambda resource, success: 
                TestAdding.__assert_creation(Todo, resource, success))
    
    