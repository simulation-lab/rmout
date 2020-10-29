import pytest


class TestTrash:

    @pytest.mark.parametrize(
        'codes_string, expected', [
            ('1, 3, 10', ['1', '3', '10']),
            ('A', ['a']),
            ('x', ['x']),
        ])
    def test_extract_target_from_userinput(self, mocker, codes_string, expected):
        from rmout import trash
        from rmout.trash import extract_target_from_userinput

        mocker.patch.object(trash, 'input', return_value=codes_string)
        codelist = extract_target_from_userinput()
        assert codelist == expected

    @pytest.fixture
    def trash_candidate(self, mocker, tmpdir):
        # test_files.py内のtest_extract_files_by_extlistと同じ

        from rmout import files
        from rmout.files import extract_files_by_extlist

        RMOUTRC = '.rmoutrc'
        current_dir = tmpdir.mkdir('rmout_test_currentdir')
        curr_rmoutrc_file = current_dir.join(RMOUTRC)
        curr_rmoutrc_file.write('.dat\n.out\n.com\n')

        target_ext_set = {'.sta', '.odb', '.com', '.msg', '.out', '.dat'}
        mocker.patch.object(files, 'sorted', return_value=target_ext_set)

        for ext in target_ext_set:
            f = current_dir.join('job1' + ext)
            f.write('test')

        return extract_files_by_extlist(target_ext_set, current_dir)

    @pytest.mark.parametrize(
        # codelist: extension's code
        # expected: file number
        'codelist, expected', [
            (['1', '2'], 2),
            (['a'], 6),
        ])
    def test_get_extensiondir_for_sendtotrash(self, _std_out, codelist, trash_candidate, expected):
        from rmout.trash import get_extensiondir_for_sendtotrash
        # check 1
        throwaway = get_extensiondir_for_sendtotrash(codelist, trash_candidate)
        assert len(throwaway) == expected
        # check 2
        ext_code = set(range(1, expected + 1))
        take_content = set([c['extension_code'] for c in throwaway])
        assert take_content == ext_code

    @pytest.mark.parametrize(
        # codelist: extension's code
        # expected: file number
        'codelist, expected', [
            (['1', '2'], 2),
            (['a'], 6),
        ])
    def test_send_to_trash(self, mocker, capfd, _std_out, codelist, trash_candidate, expected):
        from rmout import trash
        from rmout.trash import (
            get_extensiondir_for_sendtotrash,
            send_to_trash,
        )
        mocker.patch.object(trash, 'send2trash', return_value=None)
        throwaway = get_extensiondir_for_sendtotrash(codelist, trash_candidate)
        send_to_trash(throwaway, debug=False)

        out, err = capfd.readouterr()
        filelist = out.split('\n')
        filelist = [f for f in filelist if f]
        assert len(filelist) == expected
