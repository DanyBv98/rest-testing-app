import pytest

from Api import ApiResourceNotFoundError

class TestDeleting:
    def __test_resource_deletion(api, users, resources):
        for user in users:
            api.create(user)
        for resource in resources:
            assert api.delete(resource)
            with pytest.raises(ApiResourceNotFoundError):
                api.delete(resource)

    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/valid', 'user_creation.toml')
    ])
    def test_user_delete(self, api, users):
        TestDeleting.__test_resource_deletion(api, users, users)
    
    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/valid', 'post_creation.toml')
    ])
    def test_post_delete(self, api, users):
        posts = [p for u in users for p in u.posts]
        TestDeleting.__test_resource_deletion(api, users, posts)

    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/valid', 'comment_creation.toml')
    ])
    def test_comment_delete(self, api, users):
        comments = [c for u in users for p in u.posts for c in p.comments]
        TestDeleting.__test_resource_deletion(api, users, comments)

    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/valid', 'todo_creation.toml')
    ])
    def test_todo_delete(self, api, users):
        todos = [t for u in users for t in u.todos]
        TestDeleting.__test_resource_deletion(api, users, todos)
    

class TestChildrenDeleting:
    def __assert_orphan_deletion(api, users, resources):
        for user in users:
            api.create(user)
        ids = [r.id for r in resources]
        for user in users:
            api.delete(user)
        for (resource, id) in zip(resources, ids):
            with pytest.raises(ApiResourceNotFoundError):
                api.fetch(type(resource), id)

    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/valid', 'post_creation.toml')
    ])
    def test_post_delete_children(self, api, users):
        posts = [p for u in users for p in u.posts]
        TestChildrenDeleting.__assert_orphan_deletion(api, users, posts)

    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/valid', 'comment_creation.toml')
    ])
    def test_comment_delete_children(self, api, users):
        comments = [c for u in users for p in u.posts for c in p.comments]
        TestChildrenDeleting.__assert_orphan_deletion(api, users, comments)

    @pytest.mark.parametrize('test_group,test_toml', [
        ('creation/valid', 'todo_creation.toml')
    ])
    def test_todo_delete_children(self, api, users):
        todos = [t for u in users for t in u.todos]
        TestChildrenDeleting.__assert_orphan_deletion(api, users, todos)
