from typing import List, Type

from requests.models import Response
from Resource import Resource
import requests

class ApiError(Exception):
    def __init__(self, message : str) -> None:
        self.message = message
        super().__init__(self.message)

class Api:
    def __init__(self, root : str, resources : List[Type], *, access_token = None) -> None:
        for r in resources:
            if not issubclass(r, Resource):
                raise ApiError(f'Type "{r.__name__}" is not a resource.')
            if not hasattr(r, '_endpoint') or getattr(r, '_endpoint') == None:
                raise ApiError(f'Type "{r.__name__}" does not contain the _endpoint member (root endpoint for the resource).')

        self.root = root
        self.resources = resources

        self.access_token = access_token

    def __check_access_token(self) -> None:
        if not self.access_token:
            raise ApiError("An access token must be provided to the API class in order to do that.")

    def fetch(self, filter : List[Type] = None) -> List[List[Resource]]:
        if filter:
            resources_to_get = []
            for r in filter:
                if r not in self.resources:
                    raise ApiError(f'Resource "{r.__name__}" not included in the API resource list.')
                resources_to_get.append(r)
        else:
            resources_to_get = self.resources
        
        return [[r._from_dict(d) for d in requests.get(f'{self.root}{r._endpoint}').json()['data']] for r in resources_to_get]

    def create(self, resource : Resource) -> bool:
        self.__check_access_token()
        headers = {'Authorization': f'Bearer {self.access_token}'}

        response = requests.post(f'{self.root}{resource._endpoint}', resource._to_data(), headers=headers)
        resp_json = response.json()

        if response.status_code == 401:
            raise ApiError('Unauthorized to run POST requests')
        if response.status_code == 422:
            first_error = resp_json["data"][0]
            raise ApiError(f'Incomplete/Incorrect data (Field "{first_error["field"]}" {first_error["message"]})')
        
        success = response.status_code == 201
        if success:
            resource.id = resp_json['data']['id']

        return success

    def delete(self, resource : Resource) -> bool:
        self.__check_access_token()
        headers = {'Authorization': f'Bearer {self.access_token}'}

        response = requests.delete(f'{self.root}{resource._endpoint}/{resource.id}', headers=headers)
        
        if response.status_code == 401:
            raise ApiError('Unauthorized to run DELETE requests')
        if response.status_code == 404:
            raise ApiError('Resource not found.')
        
        success = response.status_code == 204
        if success:
            resource.id = None

        return success