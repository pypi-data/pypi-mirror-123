import os
import typing as tp

from take_text_preprocess.presentation import pre_process


def read_file(file_name: str, preprocess_text: bool = True) -> tp.List[str]:
    """
        Reads a list of strings from a file.
        
    :param file_name: File path.
    :type file_name: `str`
    :param preprocess_text: Flag defining the use of `take_text_preprocess`. Defaults to True.
    :type preprocess_text: `bool`
    :return: List of lines from the file.
    :rtype: `tp.List[str]`
    """
    with open(file_name, 'rb') as f:
        words = [pre_process(str(line.strip())) if preprocess_text
                 else line.strip()
                 for line in f.readlines()]
    return words


def get_files_in_dir(directory_name: str) -> tp.List['str']:
    """
        Retrieves all files from a directory.

    :param directory_name: Directory containing files to be read.
    :type directory_name: `str`
    :return: List containing all the names of the files in the directory.
    :rtype: `tp.List['str']`
    """
    try:
        return os.listdir(directory_name)
    except OSError as e:
        raise e
