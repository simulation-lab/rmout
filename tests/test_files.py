import pytest
import os


class TestFiles:

    RMOUTRC = '.rmoutrc'

    def test_get_extensions_set(self, mocker, tmpdir):
        from rmout import files
        from rmout.files import get_extensions_set

        current_dir = tmpdir.mkdir('rmout_test_currentdir')
        curr_rmoutrc_file = current_dir.join(self.RMOUTRC)
        curr_rmoutrc_file.write('.dat\n.out\n.com\n')

        home_dir = tmpdir.mkdir('rmout_test_homedir')
        home_rmoutrc_file = home_dir.join(self.RMOUTRC)
        home_rmoutrc_file.write('.odb\n.msg\n.sta\n')
        mocker.patch.object(files.pathlib.Path, 'home', return_value=home_dir)

        epected = {'.sta', '.odb', '.com', '.msg', '.out', '.dat'}
        assert get_extensions_set(current_dir) == epected

    @pytest.fixture
    def throwaway(self, tmpdir):
        return [{
            'extension_code': 1,
            'extension': '*.com',
            'file_path': ['test1.txt'],
        }]

    def test_std_out(self, throwaway):
        from rmout.files import _std_out
        assert _std_out(throwaway) == None

    def test_get_extensions_set_none(self, mocker, tmpdir):
        from rmout import files
        from rmout.files import get_extensions_set

        current_dir = tmpdir.mkdir('rmout_test_currentdir')
        current_dir.join(self.RMOUTRC)

        home_dir = tmpdir.mkdir('rmout_test_homedir')
        home_dir.join(self.RMOUTRC)
        mocker.patch.object(files.pathlib.Path, 'home', return_value=home_dir)

        epected = set()
        assert get_extensions_set(current_dir) == epected

    def test_extract_files_by_extlist(self, mocker, tmpdir, _std_out):
        from rmout import files
        from rmout.files import extract_files_by_extlist

        current_dir = tmpdir.mkdir('rmout_test_currentdir')
        curr_rmoutrc_file = current_dir.join(self.RMOUTRC)
        curr_rmoutrc_file.write('.dat\n.out\n.com\n')

        target_ext_set = {'.sta', '.odb', '.com', '.msg', '.out', '.dat'}
        mocker.patch.object(files, 'sorted', return_value=target_ext_set)

        for ext in target_ext_set:
            f = current_dir.join('job1' + ext)
            f.write('test')

        throwaway = extract_files_by_extlist(target_ext_set, current_dir)
        filelist = [file['file_path'][0] for file in throwaway]  # WindowsPath型に配慮
        filelist = [os.path.basename(str(filepath)) for filepath in filelist]
        fileset = set(filelist)
        expected = {'job1.odb', 'job1.com', 'job1.dat',
                    'job1.sta', 'job1.out', 'job1.msg'}
        assert fileset == expected

    def test_extract_files_by_extlist_none(self, mocker, tmpdir, _std_out):
        from rmout import files
        from rmout.files import extract_files_by_extlist

        current_dir = tmpdir.mkdir('rmout_test_currentdir')
        curr_rmoutrc_file = current_dir.join(self.RMOUTRC)
        curr_rmoutrc_file.write('.dat\n.out\n.com\n')

        target_ext_set = set()
        mocker.patch.object(files, 'sorted', return_value=target_ext_set)
        throwaway = extract_files_by_extlist(target_ext_set, current_dir)
        expected = list()
        assert throwaway == expected
