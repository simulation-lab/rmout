import os
import pathlib
import click
from send2trash import send2trash


@click.command()
def run():
    debug = False
    rmout(debug)
    click.echo('finished.')


def rmout(debug=True):

    # ゴミ箱送りファイルの拡張子リストを取得

    EXTENSION_FILE = '.rmoutrc'
    current_dir = os.getcwd()
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
            print(f'{target_extension_code}: {target_extension}  {len(target_files)}')
            throwaway.append({
                'extension_code': target_extension_code,
                'extension': target_extension,
                'file_path': target_files,
            })
    print('a:  all files')
    print('x:  exit')

    # input()からユーザー入力を取得し，ゴミ箱送り対象のコードリストを作成

    codes_string = input('send to trash [a]: ')
    codelist = codes_string.split(',')
    codelist = [code.strip().lower() for code in codelist]

    # ゴミ箱送りの拡張子辞書を取得

    if 'a' in codelist or '' in codelist:
        pass
    elif 'x' in codelist:
        return None
    else:
        # 不正な入力の処理
        ext_code_list = [str(target['extension_code']) for target in throwaway]
        invalid_codes = [code for code in codelist
                         if not code in ext_code_list]
        if invalid_codes:
            raise TypeError(f'The input code is invalid. {invalid_codes}')

        # ユーザー入力と一致した拡張子ファイルを抽出
        renew_throwaway = [target for target in throwaway
                           if str(target['extension_code']) in codelist]
        if renew_throwaway:
            throwaway = renew_throwaway
        else:
            raise TypeError('The input code is invalid.')

    # 削除対象のファイルをゴミ箱へ送る

    if throwaway:
        for target in throwaway:
            for target_file_path in target['file_path']:
                if debug:
                    print(os.path.basename(target_file_path))
                else:
                    print(os.path.basename(target_file_path))
                    send2trash(str(target_file_path))
