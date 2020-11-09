from click.testing import CliRunner
from rmout import core
import pytest


class TestCore:

    RMOUTRC = '.rmoutrc'

    def test_run_no_args(self, mocker):
        mocker.patch.object(core, 'rmout', return_value=None)
        runner = CliRunner()
        result = runner.invoke(core.run, [])
        expected_code = 0
        expected_output = 'finished.'
        assert result.exit_code == expected_code
        assert result.output == expected_output + '\n'

    @pytest.mark.parametrize(
        'target_ext_set, trash_candidate, throwaway', [
            (set(['.sta']),
             [{
                 'extension_code': 1,
                 'extension': '*.sta',
                 'file_path': 'test1.sta',
             }],
             [{
                 'extension_code': 1,
                 'extension': '*.sta',
                 'file_path': 'test1.sta',
             }]),
            (set(),
             [{
                 'extension_code': 1,
                 'extension': '*.sta',
                 'file_path': 'test1.sta',
             }],
             [{
                 'extension_code': 1,
                 'extension': '*.sta',
                 'file_path': 'test1.sta',
             }]),
            (set(['.sta']),
             [],
             [{
                 'extension_code': 1,
                 'extension': '*.sta',
                 'file_path': 'test1.sta',
             }]),
        ])
    def test_rmout(self, mocker, tmpdir, target_ext_set, trash_candidate, throwaway):
        from rmout import core
        from rmout.core import rmout
        from rmout.core import os
        current_dir = tmpdir.mkdir('rmout_test_currentdir')
        curr_rmoutrc_file = current_dir.join(self.RMOUTRC)
        curr_rmoutrc_file.write('.dat\n.out\n.com\n')
        mocker.patch.object(os, 'getcwd',
                            return_value=current_dir)
        mocker.patch.object(core, 'get_extensions_set',
                            return_value=target_ext_set)
        mocker.patch.object(core, 'extract_files_by_extlist',
                            return_value=trash_candidate)
        mocker.patch.object(core, 'extract_target_from_userinput',
                            return_value=['a'])
        mocker.patch.object(core, 'get_extensiondir_for_sendtotrash',
                            return_value=throwaway)
        mocker.patch.object(core, 'send_to_trash', return_value=None)
        result = rmout(debug=True)
        expected = None
        assert result == expected
