import pytest
import os


class TestFiles:

    @pytest.fixture
    def current_dir(self):
        return os.getcwd()

    def test_get_extensions_set(self, current_dir):
        from rmout.files import get_extensions_set
        target_ext_set = get_extensions_set(current_dir)
