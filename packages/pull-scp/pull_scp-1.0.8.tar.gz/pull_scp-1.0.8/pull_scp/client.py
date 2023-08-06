"""Client to handle connections and actions executed against a remote host."""
from os                     import system
from typing                 import List

from paramiko               import AutoAddPolicy, RSAKey, SSHClient
from paramiko.auth_handler  import AuthenticationException, SSHException
from scp                    import SCPClient, SCPException

from .log import LOGGER, log_formatter

import pudb

class RemoteClient:
    """Client to interact with a remote host via SSH & SCP."""

    def __init__(
        self,
        host:               str,
        user:               str,
        password:           str,
        ssh_key_filepath:   str,
        remote_path:        str,
    ):
        self.host               = host
        self.user               = user
        self.password           = password
        self.ssh_key_filepath   = ssh_key_filepath
        self.remote_path        = remote_path
        self.client             = None
        self.localpath          = ''
        self.verbosity          = 0
        self._upload_ssh_key()

    @property
    def connection(self):
        """Open SSH connection to remote host."""
        try:
            client = SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(
                self.host,
                username        =   self.user,
                password        =   self.password,
                key_filename    =   self.ssh_key_filepath,
                timeout         =   5000,
            )
            self.client     = client
            return client
        except AuthenticationException as e:
            LOGGER.error(
                f"AuthenticationException occurred; did you remember to generate an SSH key? {e}"
            )
            raise e
        except Exception as e:
            LOGGER.error(f"Unexpected error occurred: {e}")
            raise e

    @property
    def scp(self) -> SCPClient:
        conn = self.connection
        return SCPClient(conn.get_transport())

    def _get_ssh_key(self):
        """Fetch locally stored SSH key."""
        try:
            self.ssh_key = RSAKey.from_private_key_file(self.ssh_key_filepath)
            LOGGER.info(f"Found SSH key at self {self.ssh_key_filepath}")
            return self.ssh_key
        except SSHException as e:
            LOGGER.error(e)
        except Exception as e:
            LOGGER.error(f"Unexpected error occurred: {e}")
            raise e

    def _upload_ssh_key(self):
        try:
            system(
                f"ssh-copy-id -i {self.ssh_key_filepath}.pub {self.user}@{self.host}>/dev/null 2>&1"
            )
            LOGGER.info(f"{self.ssh_key_filepath} uploaded to {self.host}")
        except FileNotFoundError as error:
            LOGGER.error(error)
        except Exception as e:
            LOGGER.error(f"Unexpected error occurred: {e}")
            raise e

    def disconnect(self):
        """Close SSH & SCP connection."""
        if self.connection:
            self.client.close()
        if self.scp:
            self.scp.close()

    def bulk_upload(self, files: List[str]):
        """
        Upload multiple files to a remote directory.

        :param files: List of local files to be uploaded.
        :type files: List[str]
        """
        try:
            self.scp.put(files, remote_path=self.remote_path, recursive=True)
            LOGGER.info(
                f"Finished uploading {len(files)} files to {self.remote_path} on {self.host}"
            )
        except SCPException as e:
            raise e

    def bulk_pullObj(self, l_obj : list) -> dict:
        b_status    : bool  = False
        d_ret       = {
            'status'    : b_status,
            'pulled'    : []
        }

        for o in l_obj:
            self.filepath_get(o)
            d_ret['pulled'].append(o)
        if len(d_ret['pulled']):
            b_status    = True
        d_ret['status'] = b_status
        return d_ret

    def filepath_get(self, filepath: str):
        """Download filepath from remote host."""
        if self.verbosity:
            LOGGER.info("Pulling %s@%s:%s..." % (self.user, self.host, filepath))
        try:
            self.scp.get(filepath, local_path = self.localpath, recursive = True)
        except Exception as e:
            LOGGER.error("An error occured executing %s! Perhaps this is a special file?" % e)

    def commandList_exec(self, commands: List[str], b_quiet: bool = False) -> list:
        """
        Execute multiple commands in succession.

        :param commands: List of unix commands as strings.
        :type commands: List[str]
        """
        l_ret:      list    = []
        l_stdin:    list    = []
        l_stdout:   list    = []
        l_stderr:   list    = []
        for cmd in commands:
            stdin, stdout, stderr = self.connection.exec_command(cmd)
            stdout.channel.recv_exit_status()
            try:
                l_stdin     = [f.rstrip() for f in stdin.readlines()]
            except:
                pass
            l_stdout    = [f.rstrip() for f in stdout.readlines()]
            l_stderr    = [f.rstrip() for f in stderr.readlines()]
            if not b_quiet:
                for line in l_stdout:
                        LOGGER.trace(f"(remote): {cmd}")
                        LOGGER.info(f"(remote): {cmd}: {line}")
            l_ret.append( {
                'stdin'     : l_stdin,
                'stdout'    : l_stdout,
                'stderr'    : l_stderr
            })
        return l_ret
