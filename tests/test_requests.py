# Copyright 2024 Sergio Tejedor Moreno

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
import requests

from earthquakelocator.request import make_request

def test_make_request_success(requests_mock, today_url):
    """ Prueba que la función retorna correctamente 
    la respuesta JSON cuando el estado HTTP es 200. """

    mock_response = {'key': 'value'}
    requests_mock.get(today_url, json=mock_response, status_code=200)

    response = make_request(today_url)
    assert response == mock_response, "La función debería haber retornado la respuesta JSON correctamente."


def test_make_request_failure(requests_mock, today_url):
    """ Prueba que la función retorna None cuando el estado HTTP no es 200. """

    requests_mock.get(today_url, status_code=404)
    response = make_request(today_url)
    assert response is None, "La función debería haber retornado None debido al código de estado 404."


def test_make_request_exception(requests_mock, today_url):
    """ Prueba el manejo de excepciones si hay un error de conexión. """

    requests_mock.get(today_url, exc=requests.exceptions.ConnectionError)
    with pytest.raises(requests.exceptions.ConnectionError):
        make_request(today_url)