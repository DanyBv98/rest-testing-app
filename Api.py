from typing import List, Type

from requests.models import Response
from Resource import Resource
import requests

class ApiError(Exception):
    def __init__(self, message : str) -> None:
        self.message = message
        super().__init__(self.message)

class ApiResourceInitializationError(ApiError):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class ApiInvalidAccessTokenError(ApiError):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class ApiIncorrectDataError(ApiError):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class ApiResourceIdNotEmptyError(ApiError):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        
class ApiResourceNotFoundError(ApiError):
    def __init__(self, resource_type : Type, id : int) -> None:
        super().__init__(f'Resource {resource_type.__name__} with id {id} could not be found.')


class Api:
    def __init__(self, root : str, resources : List[Type], *, access_token = None) -> None:
        for r in resources:
            if not issubclass(r, Resource):
                raise ApiResourceInitializationError(f'Type "{r.__name__}" is not a resource.')
            if not hasattr(r, '_endpoint') or getattr(r, '_endpoint') == None:
                raise ApiResourceInitializationError(f'Type "{r.__name__}" does not contain the _endpoint member (root endpoint for the resource).')

        self.root = root
        self.resources = resources

        self.access_token = access_token
        self.__resources_pool = {r : {} for r in resources}

        self.__own_resources = []

    def __check_access_token(self) -> None:
        if not self.access_token:
            raise ApiInvalidAccessTokenError("An access token must be provided to the API class in order to do that.")
    
    def fetch(self, resource_type : Type, id : int = None) -> List[Resource] | Resource:
        if id:
            response = requests.get(f'{self.root}{resource_type._endpoint}/{id}')
            if response.status_code == 404:
                raise ApiResourceNotFoundError(resource_type, id)
            if response.status_code == 200:
                self.__resources_pool[resource_type][id] = resource_type._from_dict(response.json()['data'])
                return self.__resources_pool[resource_type][id]
        else:
            response = requests.get(f'{self.root}{resource_type._endpoint}')
            if response.status_code != 200:
                raise ApiError(f'Unknown error occured. Got {response.status_code} when fetching data.')
            data = response.json()['data']

            self.__resources_pool[resource_type].clear()
            for d in data:
                resource = resource_type._from_dict(d) 
                self.__resources_pool[resource_type][resource.id] = resource
            return list(self.__resources_pool[resource_type].values())

    def get(self, resource_type : Type, id : int, force_update = False) -> Resource:
        if not force_update and id in self.__resources_pool[resource_type]:
            return self.__resources_pool[resource_type][id]
        else:
            return self.fetch(resource_type, id)

    def create(self, resource : Resource) -> bool:
        self.__check_access_token()
        headers = {'Authorization': f'Bearer {self.access_token}'}
        
        if resource.id != None:
            raise ApiResourceIdNotEmptyError('A resource object that needs to be created cannot have an id.')

        response = requests.post(f'{self.root}{resource._endpoint}', resource._to_data(), headers=headers)
        resp_json = response.json()

        if response.status_code == 401:
            raise ApiInvalidAccessTokenError('Unauthorized to run POST requests')
        if response.status_code == 422:
            first_error = resp_json["data"][0]
            raise ApiIncorrectDataError(f'Field "{first_error["field"]}" {first_error["message"]}.')
        
        success = response.status_code == 201
        if success:
            resource.id = resp_json['data']['id']
            self.__resources_pool[type(resource)][resource.id] = resource
            self.__own_resources.append(resource)

        return success

    def delete(self, resource : Resource) -> bool:
        self.__check_access_token()
        headers = {'Authorization': f'Bearer {self.access_token}'}

        response = requests.delete(f'{self.root}{resource._endpoint}/{resource.id}', headers=headers)
        
        if response.status_code == 401:
            raise ApiInvalidAccessTokenError('Unauthorized to run DELETE requests')
        if response.status_code == 404:
            raise ApiResourceNotFoundError(type(resource), resource.id)
        
        success = response.status_code == 204
        if success:
            if resource.id in self.__resources_pool[type(resource)]:
                del self.__resources_pool[type(resource)][resource.id]
            resource.id = None

            if resource in self.__own_resources:
                self.__own_resources.remove(resource)

        return success
    
    def cleanup(self) -> None:
        for r in self.__own_resources:
            self.delete(r)
        self.__own_resources.clear()
