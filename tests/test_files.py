import pytest
import os


class TestFiles:

    def test_current_dir(self, mocker, tmpdir_factory):
        from rmout import files
        from rmout.files import get_extensions_set

        RMOUTRC = '.rmoutrc'
        current_dir = tmpdir_factory.mktemp('rmout_test_currentdir')
        curr_rmoutrc_file = current_dir.join(RMOUTRC)
        curr_rmoutrc_file.write('.dat\n.out\n.com\n')

        home_dir = tmpdir_factory.mktemp('rmout_test_homedir')
        home_rmoutrc_file = home_dir.join(RMOUTRC)
        home_rmoutrc_file.write('.odb\n.msg\n.sta\n')
        mocker.patch.object(files.pathlib.Path, 'home', return_value=home_dir)

        epected = {'.sta', '.odb', '.com', '.msg', '.out', '.dat'}

        assert get_extensions_set(current_dir) == epected

    def test_tmpdir(self, tmpdir):
        a_sub_dir = tmpdir.mkdir('anything')
        a_file = a_sub_dir.join('something.txt')
        another_file = a_sub_dir.join('something_else.txt')
        a_file.write('contents may settle during shipping')
        another_file.write('something different')

        assert a_file.read() == 'contents may settle during shipping'
        assert another_file.read() == 'something different'

    def test_create_file(self, tmpdir):
        p = tmpdir.mkdir("sub").join("hello.txt")
        p.write("content")
        assert p.read() == "content"
        assert len(tmpdir.listdir()) == 1

    # def test_get_extensions_set(self, current_dir):
    #     from rmout.files import get_extensions_set
        # target_ext_set = get_extensions_set(current_dir)
        # print(current_dir.read())

        # assert current_dir.read() == '.dat\n.out\n.com\n'
