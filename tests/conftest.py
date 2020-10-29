import pytest


@pytest.fixture
def _std_out(mocker):
    from rmout import files
    mocker.patch.object(files, '_std_out', return_value=None)
