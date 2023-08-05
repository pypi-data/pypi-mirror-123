from __future__ import annotations

from time import sleep
from typing import Optional

import requests

from .config import API_KEY
from .constants import BASEURL
from .exceptions import (APIObjectNotFound,
                         APIRequestNotValid, BadGatewayError,
                         HandlingResponseError,
                         ServiceNotImplementedError, ServiceUnavailableError,
                         UnexpectedServerError)


class RequestsHelper:
    """Interface for handling requests."""
    @classmethod
    def get(cls, id: str, endpoint: str) -> dict:
        """Creates a GET request for the supplied id and endpoint.

        Args:
            id (str): Used to indentify the endpoint instance.
            endpoint (str): One of the DynaCrop API endpoints.

        Returns:
            dict: Reponse to the request.
        """
        r = requests.get(
            cls.build_url(endpoint, id),
            params={'api_key': API_KEY})
        return cls.handle_response(r)

    @classmethod
    def patch(cls, id: str, data: dict, endpoint: str) -> dict:
        """Creates a PATCH request for the supplied id, endpoint
    and patch data.

        Args:
            id (str): Used to indentify the endpoint instance.
            data (dict): Used to patch the existing backend data.
            endpoint (str): One of the DynaCrop API endpoints.


        Returns:
            dict: Response to the request with patched data.
        """
        r = requests.patch(
            cls.build_url(endpoint, id),
            params={'api_key': API_KEY}, data=data)
        return cls.handle_response(r)

    @classmethod
    def post(cls, data: dict, endpoint: str) -> dict:
        """Creates a POST request for the supplied id, endpoint and post data.

        Args:
            id (str): Used to indentify the endpoint instance.
            data (dict): Used to create new instance of the endpoint
            on the backend.
            endpoint (str): One of the DynaCrop API endpoints.


        Returns:
            dict: Response to the request with a new instance
            of endpoint.
        """
        r = requests.post(
            cls.build_url(endpoint),
            params={'api_key': API_KEY},
            data=data)
        return cls.handle_response(r)

    @classmethod
    def handle_response(cls, response: requests.Response):
        """Handles response from the request methods.

        Args:
            response (dict): Reponse supplied via request methods
            of the RequestHelper class

        Raises:
            APIObjectNotFound: 404 Not Found. Might be a non-existent
                response content or a API-side error.
            APIRequestNotValid: 400 Bad Request. Might be a wrongly
                defined request.
            UnexpectedServerError: 500 Internal Server Error. Might be an API
                error that can only be resolved on server side.
            ServiceNotImplementedError: 501 Not Implemented. The request was
                not recognized by the API server. Might be implemented
                in the future.
            BadGatewayError: 502 Bad Gateway. There could have been an error
                beyond the DynaCrop API.
            ServiceUnavailableError: 503 Service Unavailable. The API
                is temporarily unavailable.
            HandlingResponseError: Some other unrecognized error.

        Returns: None
        """
        if response.status_code == 200 or response.status_code == 201:
            # TODO check for id
            # I do not understand.
            return response.json()
        elif response.status_code == 404:
            raise APIObjectNotFound(response.url)
        elif response.status_code == 400:
            raise APIRequestNotValid(response.json())
        elif response.status_code == 500:
            raise UnexpectedServerError
        elif response.status_code == 501:
            raise ServiceNotImplementedError
        elif response.status_code == 502:
            raise BadGatewayError
        elif response.status_code == 503:
            raise ServiceUnavailableError
        else:
            raise HandlingResponseError

    @classmethod
    def build_url(cls, *args: Optional[str]) -> str:
        """Builds internet url based on parameters

        Returns:
            str: Built URL.
        """
        return '/'.join([BASEURL] + [str(x) for x in args])


class APIObject:
    """Metaclass for various endpoints of the API."""
    editable_attrs: Optional[set] = {}
    endpoint: str = ""
    object_attrs: Optional[set] = {'data', 'id'}

    def __init__(self, id: str):
        """Constructs an API object.

        Args:
            id (str): ID of an endpoint request.
        """
        self.id: str = id
        self.data: Optional[dict] = {}
        self.refresh()

    def __getattr__(self, item: str):
        """An override for getattr.

        Args:
            item (str): Attribute to be found from the object

        Raises:
            AttributeError: If attribute not found.

        Returns:
            Any: None
        """
        if item in self.data:
            return self.data[item]
        else:
            raise AttributeError(item)

    def __setattr__(self, key: str, value: str):
        """An override for setattr.

        Args:
            key (str): The name of the attribute.
            value (str): The value of the attribute.

        Raises:
            AttributeError: If accessed a non-editable attribute .
        """
        if key in self.__class__.object_attrs:
            super(APIObject, self).__setattr__(key, value)

        else:
            if key in self.__class__.editable_attrs:
                self.data[key] = value
                self.data = RequestsHelper.patch(
                    self.id,
                    {key: self.data[key]
                        for key
                        in self.__class__.editable_attrs},
                    self.endpoint)
            else:
                raise AttributeError

    @classmethod
    def get(cls, id: str) -> APIObject:
        """Acquires APIObject instatiated into one of the DynaCrop API endpoints.

        Args:
            id (str): ID of an endpoint request.

        Returns:
            APIObject: APIObject made to an API endpoint.
        """
        return cls(id)

    @classmethod
    def create(cls, **kwargs: Optional[str]) -> APIObject:
        """Creates APIObject later instatiated into one of the DynaCrop API endpoints.

        Args:
            kwargs (Optional[str])

        Returns:
            APIObject: APIObject made to an API endpoint.
        """
        return cls.get(RequestsHelper.post(
            {key: val for key, val in kwargs.items() if val},
            cls.endpoint)['id'])

    def is_ready(self) -> bool:
        """Checks whether the request is ready.

        Returns:
            bool: Is ready statement.
        """
        self.refresh()

        return self.data['status'] != 'created' \
            or self.data['status'] != 'rendering'

    def is_failed(self) -> bool:
        """Checks whether the request failed.

        Returns:
            bool: Failure statement.
        """
        return self.data['status'] == 'error'

    def block_till_completed(self, polling_interval: int = 1):
        """Suspends the code execution until the request response is
    returned as finished/with error/with no data.

        Args:
            polling_interval (int, optional): Time to wait between
            checking iterations. Defaults to 1.
        """
        while not self.is_ready():
            sleep(polling_interval)

    def refresh(self):
        """Updates response data."""
        self.data = RequestsHelper.get(self.id, self.__class__.endpoint)

    def __eq__(self, other: APIObject) -> bool:
        """Compares two instantiated endpoints (APIObjects).

        Args:
            other (APIObject): Another APIObject to compare.

        Returns:
            bool: Comparation statement.
        """
        return other.id == self.id

    def __str__(self) -> str:
        """Returns structured information about APIObject.

        Returns:
            str: Structured information about APIObject.
        """
        return f"<dynacrop.{self.__class__.__name__} {self.id}>"
