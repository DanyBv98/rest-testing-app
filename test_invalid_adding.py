import pytest
from Api import ApiIncorrectDataError

class TestInvalidAddingDuplicate:
    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/invalid/duplicate', 'duplicate_email.toml')
    ])
    def test_invalid_user_adding(self, api, users):
        api.create(users[0])
        with pytest.raises(ApiIncorrectDataError):
            api.create(users[1])

class TestInvalidAddingMissingFields:
    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/invalid/missing_fields', 'users_missing.toml')
    ])
    def test_invalid_user_adding(self, api, users):
        for user in users:
            with pytest.raises(ApiIncorrectDataError):
                api.create(user)
    
    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/invalid/missing_fields', 'posts_missing.toml')
    ])
    def test_invalid_post_adding(self, api, users):
        posts = [p for u in users for p in u.posts]
        for user in users:
            api.create(user, create_children=False)
        for post in posts:
            with pytest.raises(ApiIncorrectDataError):
                api.create(post)

    
    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/invalid/missing_fields', 'comments_missing.toml')
    ])
    def test_invalid_comment_adding(self, api, users):
        posts = [p for u in users for p in u.posts]
        comments = [c for p in posts for c in p.comments]
        for user in users:
            api.create(user, create_children=False)
            for post in posts:
                api.create(post, create_children=False)
        for comment in comments:
            with pytest.raises(ApiIncorrectDataError):
                api.create(comment)

    
    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/invalid/missing_fields', 'todos_missing.toml')
    ])
    def test_invalid_todo_adding(self, api, users):
        todos = [t for u in users for t in u.todos]
        for user in users:
            api.create(user, create_children=False)
            for todo in todos:
                with pytest.raises(ApiIncorrectDataError):
                    api.create(todo)

class TestInvalidAddingMissingParent:
    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/invalid/missing_parent', 'posts_missing.toml')
    ])
    def test_invalid_post_adding(self, api, posts):
        for post in posts:
            with pytest.raises(ApiIncorrectDataError):
                api.create(post)

    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/invalid/missing_parent', 'comments_missing.toml')
    ])
    def test_invalid_comment_adding(self, api, comments):
        for comment in comments:
            with pytest.raises(ApiIncorrectDataError):
                api.create(comment)
    
    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/invalid/missing_parent', 'todos_missing.toml')
    ])
    def test_invalid_todo_adding(self, api, todos):
        for todo in todos:
            with pytest.raises(ApiIncorrectDataError):
                api.create(todo)
