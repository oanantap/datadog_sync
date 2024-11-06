import requests
from config.config import (
    SOURCE_APPLICATION_KEY, SOURCE_API_KEY, DESTINATION_API_KEY,
    DESTINATION_APPLICATION_KEY
)


class APIClient:
    def __init__(self, api_key, app_key, type):
        self.api_key = api_key
        self.app_key = app_key
        self.type = type

    def get_headers(self):
        if self.type == 'import':
            API_KEY = SOURCE_API_KEY
            APPLICATION_KEY = SOURCE_APPLICATION_KEY
        else:
            API_KEY = DESTINATION_API_KEY
            APPLICATION_KEY = DESTINATION_APPLICATION_KEY

        return {
            'DD-API-KEY': API_KEY,
            'DD-APPLICATION-KEY': APPLICATION_KEY,
            'Content-Type': 'application/json'
        }

    def get(self, url):
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response

    def post(self, url, body):
        headers = self.get_headers()
        response = requests.post(url, body, headers=headers)
        response.raise_for_status()
        return response

    def validate_api(self, url):
        try:
            response = self.get(url)
            print(response.text)
            print("Validate source API successful.")
        except Exception as e:
            print(f"DD failed to validate the API {url}. Error: {str(e)}")
