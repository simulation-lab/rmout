import os
import sys
import pathlib
import click
from send2trash import send2trash


@click.command()
def run():
    debug = True
    rmout(debug)
    click.echo('finished.')


def rmout(debug=True):

    current_dir = os.getcwd()

    def get_extensions_set(current_dir) -> set:
        # ゴミ箱送りファイルの拡張子リストを取得

        EXTENSION_FILE = '.rmoutrc'
        home_dir = pathlib.Path.home()
        extfile_in_curr = os.path.join(current_dir, EXTENSION_FILE)
        extfile_in_home = os.path.join(home_dir, EXTENSION_FILE)

        target_ext_list = []
        if os.path.isfile(extfile_in_home):
            with open(extfile_in_home, 'r') as f:
                target_ext_list += [e.strip() for e in f.readlines()]
        if os.path.isfile(extfile_in_curr):
            with open(extfile_in_curr, 'r') as f:
                target_ext_list += [e.strip() for e in f.readlines()]
        target_ext_set = set(target_ext_list)
        return target_ext_set

    target_ext_set = get_extensions_set(current_dir)

    def extract_files_by_extlist(target_ext_set) -> list:
        # カレントディレクトリから拡張子リストに対応したファイルを抽出

        throwaway = []
        target_extension_code = 0
        for extension in sorted(target_ext_set):
            target_extension = '*' + extension
            target_files = pathlib.Path(current_dir).glob(target_extension)
            target_files = [f for f in target_files
                            if os.path.isfile(os.path.join(current_dir, f))]
            if target_files:
                target_extension_code += 1
                throwaway.append({
                    'extension_code': target_extension_code,
                    'extension': target_extension,
                    'file_path': target_files,
                })

        for target in throwaway:
            print(
                f'{target["extension_code"]:6}: {target["extension"]}  {len(target["file_path"])}')
        print(f'{"":5}a: all files')
        print(f'{"":5}x: exit')
        return throwaway

    throwaway = extract_files_by_extlist(target_ext_set)

    def extract_target_from_userinput() -> list:
        # input()からユーザー入力を取得し，ゴミ箱送り対象のコードリストを作成

        codes_string = input('send to trash [a]: ')
        codes_string = codes_string.strip()  # .strip(',')
        codelist = codes_string.split(',')
        if len(set(codelist)) != len(codelist):
            try:
                raise ValueError('The input code may be duplicated.')
            except ValueError as e:
                print(f'{e} {codelist}')
                sys.exit()
        codelist = [code.strip().lower() for code in codelist]
        return codelist

    codelist = extract_target_from_userinput()

    def get_extensiondir_for_sendtotrash(codelist, throwaway) -> list:
        # ゴミ箱送りの拡張子辞書を取得

        if 'a' in codelist or '' in codelist:
            pass
        elif 'x' in codelist:
            return list()
        else:
            # 不正な入力の処理
            ext_code_list = [str(target['extension_code'])
                             for target in throwaway]
            invalid_codes = [code for code in codelist
                             if not code in ext_code_list]
            if invalid_codes:
                try:
                    raise ValueError('The input code is invalid.')
                except ValueError as e:
                    print(f'{e} {invalid_codes}')
                    sys.exit()

            # ユーザー入力と一致した拡張子ファイルを抽出
            renew_throwaway = [target for target in throwaway
                               if str(target['extension_code']) in codelist]
            throwaway = renew_throwaway
        return throwaway

    throwaway = get_extensiondir_for_sendtotrash(codelist, throwaway)

    def send_to_trash(throwaway):
        # 削除対象のファイルをゴミ箱へ送る

        if throwaway:
            for target in throwaway:
                for target_file_path in target['file_path']:
                    if debug:
                        print(os.path.basename(target_file_path))
                    else:
                        print(os.path.basename(target_file_path))
                        send2trash(str(target_file_path))

    send_to_trash(throwaway)
