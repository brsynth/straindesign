from tempfile import _TemporaryFileWrapper

# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pytest
import requests
from pandas import DataFrame

from cameobrs.models.webmodels import (
    NotFoundException,
    get_sbml_file,
    index_models_minho,
)


class TestWebModels:
    def test_invalid_host(self):
        with pytest.raises(requests.ConnectionError):
            index_models_minho(host="http://blabla")
        with pytest.raises(requests.ConnectionError):
            get_sbml_file(1, host="http://blabla")

    @pytest.mark.skipif(True, reason="too slow for testing")
    def test_index(self):
        try:
            index = index_models_minho()
        except requests.ConnectionError:
            pytest.skip("skipping test due to connection error")
        else:
            assert isinstance(index, DataFrame)
            assert list(index.columns) == [
                "id",
                "name",
                "doi",
                "author",
                "year",
                "formats",
                "organism",
                "taxonomy",
                "validated",
            ]

    @pytest.mark.skipif(True, reason="too slow for testing")
    def test_get_sbml(self):
        try:
            tmp = get_sbml_file(1)
        except requests.ConnectionError:
            pytest.skip("skipping test due to connection error")
        else:
            assert isinstance(tmp, _TemporaryFileWrapper)
            with pytest.raises(NotFoundException):
                get_sbml_file(-1)
