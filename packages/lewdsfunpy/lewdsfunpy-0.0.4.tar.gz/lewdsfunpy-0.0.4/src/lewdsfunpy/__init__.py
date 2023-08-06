from dotenv import dotenv_values
import requests
config = dotenv_values(".env")

Lewds_API_KEY = config.get('Lewds_API_KEY', None)


class APIKeyMissingError(Exception):
    pass


if Lewds_API_KEY is None:
    raise APIKeyMissingError(
        "All methods require an API key. See "
        "https://docs.lewds.fun/api/api-keys "
        "for how to retrieve an authentication token from "
        "Lewds API and make a .env file "
        "with your key and value"
        "ex:  Lewds_API_KEY=YOURAPITOKENHERE"
    )

session = requests.Session()
session.params = {}
session.headers['authorization'] = Lewds_API_KEY

from .lewds import LewdsAPI