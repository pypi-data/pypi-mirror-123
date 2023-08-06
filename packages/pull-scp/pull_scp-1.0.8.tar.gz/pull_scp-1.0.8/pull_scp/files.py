"""Find local files to be uploaded to remote host."""
from os         import walk
from typing     import List

from .config    import LOCAL_FILE_DIRECTORY


def list_localFiles(str_localDir: str) -> List[str]:
    """
    Create list of file paths.

    :param str_localDir: Local filepath of assets to SCP to host.
    :type str_localDir: List[str]
    """
    local_files = walk(str_localDir)
    for root, dirs, files in local_files:
        return [f"{LOCAL_FILE_DIRECTORY}/{file}" for file in files]
