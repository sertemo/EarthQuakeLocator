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

from datetime import datetime, timedelta

import pytest


@pytest.fixture(scope="session")
def today_url():
    starttime = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    endtime = datetime.strftime(datetime.today(), "%Y-%m-%d")
    URL_BASE = "https://earthquake.usgs.gov/fdsnws/event/1/"
    query = f"query?format=geojson&starttime={starttime}&endtime={endtime}"
    URL = URL_BASE + query
    return URL
