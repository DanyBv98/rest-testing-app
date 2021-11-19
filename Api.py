from typing import Dict, List, Type

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

class ApiResourceTypeNotFoundError(ApiError):
    def __init__(self, resource_type : Type) -> None:
        super().__init__(f'The "{resource_type.__name__}" resource does not exist in the current API.')
        
class ApiResourceNotFoundError(ApiError):
    def __init__(self, resource_type : Type, id : int) -> None:
        super().__init__(f'Resource {resource_type.__name__} with id {id} could not be found.')


class Api:
    def __init__(self, root : str, *, access_token = None, endpoints : Dict[Type, str] = {}) -> None:
        self.root = root
        self.access_token = access_token

        self.__endpoints      : Dict[Type, str]                 = {}
        self.__resources_pool : Dict[Type, Dict[int, Resource]] = {}
        self.__own_resources  : List[Resource ]                 = []

        for r in endpoints:
            self.add_resource(r, endpoints[r])

    def add_resource(self, resource_type : Type, endpoint : str) -> None:
        if resource_type in self.__resources_pool:
            raise ApiResourceInitializationError(f'Resource "{resource_type.__name__}" has already been added.')

        if not issubclass(resource_type, Resource):
            raise ApiResourceInitializationError(f'Type "{resource_type.__name__}" is not a resource.')
        
        self.__endpoints[resource_type] = endpoint
        self.__resources_pool[resource_type] = {}

    def __check_access_token(self) -> None:
        if not self.access_token:
            raise ApiInvalidAccessTokenError("An access token must be provided to the API class in order to do that.")
    
    def __check_resource_type(self, resource_type : Type) -> None:
        if resource_type not in self.__resources_pool:
            raise ApiResourceTypeNotFoundError(resource_type)

    def fetch(self, resource_type : Type, id : int = None) -> List[Resource] | Resource:
        self.__check_resource_type(resource_type)
        if id:
            response = requests.get(f'{self.root}{self.__endpoints[resource_type]}/{id}')
            if response.status_code == 404:
                raise ApiResourceNotFoundError(resource_type, id)
            if response.status_code != 200:
                raise ApiError(f'Unknown error occured. Got {response.status_code} when fetching data.')

            self.__resources_pool[resource_type][id] = resource_type._from_dict(response.json()['data'])
            return self.__resources_pool[resource_type][id]
            
        else:
            response = requests.get(f'{self.root}{self.__endpoints[resource_type]}')
            if response.status_code != 200:
                raise ApiError(f'Unknown error occured. Got {response.status_code} when fetching data.')
            data = response.json()['data']

            self.__resources_pool[resource_type].clear()
            for d in data:
                resource = resource_type._from_dict(d) 
                self.__resources_pool[resource_type][resource.id] = resource
            return list(self.__resources_pool[resource_type].values())

    def get(self, resource_type : Type, id : int, force_update = False) -> Resource:
        self.__check_resource_type(resource_type)
        
        if not force_update and id in self.__resources_pool[resource_type]:
            return self.__resources_pool[resource_type][id]
        else:
            return self.fetch(resource_type, id)

    def create(self, resource : Resource) -> bool:
        self.__check_access_token()
        self.__check_resource_type(type(resource))

        headers = {'Authorization': f'Bearer {self.access_token}'}
        
        if resource.id != None:
            raise ApiResourceIdNotEmptyError('A resource object that needs to be created cannot have an id.')

        response = requests.post(f'{self.root}{self.__endpoints[type(resource)]}', resource._to_data(), headers=headers)
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
        self.__check_resource_type(type(resource))

        headers = {'Authorization': f'Bearer {self.access_token}'}

        response = requests.delete(f'{self.root}{self.__endpoints[type(resource)]}/{resource.id}', headers=headers)
        
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
