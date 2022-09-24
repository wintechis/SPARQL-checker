from config import *

def create_files_txt() -> None:
    with open(IDM_FILE, 'r') as f:
        user_names = [line.strip() for line in f.readlines()]
    lst = []
    for user in user_names:
        for file_name in FILE_NAMES:
            lst.append(f'{PAUL_DIR}{user}/{file_name}\n')

    with open(FILES_FILE, 'w') as f:
        f.writelines(lst)