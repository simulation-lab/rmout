from click.testing import CliRunner
from rmout import core


def test_run_no_args(mocker):
    mocker.patch.object(core, 'rmout', return_value=None)
    runner = CliRunner()
    result = runner.invoke(core.run, [])
    expected_code = 0
    expected_output = 'finished.'
    assert result.exit_code == expected_code
    assert result.output == expected_output + '\n'
