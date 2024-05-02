from typing import Any

import requests


def make_request(url: str) -> Any | None:
    """Lanza la request y devuelve una respuesta
    en formato json

    Parameters
    ----------
    url : str
        _description_

    Returns
    -------
    requests.Response
        _description_
    """
    response = requests.get(url)

    if response.status_code != 200:
        print(response)
        print(response.status_code)
        return None

    return response.json()
