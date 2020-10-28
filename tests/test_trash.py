

class TestTrash:

    def test_extract_target_from_userinput(self, mocker):
        from rmout import trash
        from rmout.trash import extract_target_from_userinput

        codes_string = '1, 3, 10'
        mocker.patch.object(trash, 'input', return_value=codes_string)
        codelist = extract_target_from_userinput()
        expected = ['1', '3', '10']
        assert codelist == expected

    def test_get_extensiondir_for_sendtotrash(self, mocker):
        pass

    def test_send_to_trash(self, mocker):
        pass
