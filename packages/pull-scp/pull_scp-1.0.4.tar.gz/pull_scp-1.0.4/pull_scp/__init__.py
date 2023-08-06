"""Perform tasks against a remote host."""
from typing     import List

from .config    import LOCAL_FILE_DIRECTORY

from .client    import RemoteClient

def localfiles_uploadToRemote(ssh_remote_client: RemoteClient, l_localpath: List[str]):
    """Do a recursive upload to remote on each element in the <l_localpath>

    Args:
        ssh_remote_client (RemoteClient): the ssh/scp client instance
        l_localpath (List[str]): a list of localpath(s) to push
    """
    ssh_remote_client.bulk_upload(l_localpath)

def commandList_execOnRemote(
    ssh_remote_client:  RemoteClient,
    l_commands:         List[str]       = None,
    b_quiet:            bool            = False
) -> list:
    """
    Execute UNIX command on the remote host. Commands are passed as a
    list -- each list element is executed in turn.

    :param ssh_remote_client: Remote server.
    :type ssh_remote_client: RemoteClient
    :param commands: List of commands to run on remote host.
    :type commands: List[str]
    """
    l_ret  : list = ssh_remote_client.commandList_exec(l_commands, b_quiet)
    return l_ret
