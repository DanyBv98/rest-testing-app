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
    def __assert_missing_field_incorrect(api, resources):
        for resource in resources:
            with pytest.raises(ApiIncorrectDataError):
                api.create(resource)

    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/invalid/missing_fields', 'users_missing.toml')
    ])
    def test_invalid_user_adding(self, api, users):
        TestInvalidAddingMissingFields.__assert_missing_field_incorrect(api, users)
    
    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/invalid/missing_fields', 'posts_missing.toml')
    ])
    def test_invalid_post_adding(self, api, users):
        posts = [p for u in users for p in u.posts]
        for user in users:
            api.create(user, create_children=False)
        TestInvalidAddingMissingFields.__assert_missing_field_incorrect(api, posts)

    
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
        TestInvalidAddingMissingFields.__assert_missing_field_incorrect(api, comments)

    
    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/invalid/missing_fields', 'todos_missing.toml')
    ])
    def test_invalid_todo_adding(self, api, users):
        todos = [t for u in users for t in u.todos]
        for user in users:
            api.create(user, create_children=False)
        TestInvalidAddingMissingFields.__assert_missing_field_incorrect(api, todos)

class TestInvalidAddingMissingParent:
    def __assert_missing_parents_incorrect(api, resources):
        for resource in resources:
            with pytest.raises(ApiIncorrectDataError):
                api.create(resource)
    
    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/invalid/missing_parent', 'posts_missing.toml')
    ])
    def test_invalid_post_adding(self, api, posts):
        TestInvalidAddingMissingParent.__assert_missing_parents_incorrect(api, posts)

    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/invalid/missing_parent', 'comments_missing.toml')
    ])
    def test_invalid_comment_adding(self, api, comments):
        TestInvalidAddingMissingParent.__assert_missing_parents_incorrect(api, comments)
    
    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/invalid/missing_parent', 'todos_missing.toml')
    ])
    def test_invalid_todo_adding(self, api, todos):
        TestInvalidAddingMissingParent.__assert_missing_parents_incorrect(api, todos)
