from typing import List
from file_handling import save_file

def edit_files_file(idms: List[str], f_files: str, base: str, include_idm: bool, filenames: List[str]) -> None:
    files = [f'{base}{idm}/{name}' for idm in idms for name in filenames] if include_idm else [f'{base}{name}' for name in filenames]
    save_file(f_files, '\n'.join(files), mode='w')