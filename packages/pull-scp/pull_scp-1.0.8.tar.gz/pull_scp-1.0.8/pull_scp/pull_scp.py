#
# pull_scp FS ChRIS plugin app
#
# (c) 2021 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import                          os

from paramiko.client    import  SSHClient
from chrisapp.base      import  ChrisApp

from subprocess         import  run

from .                  import  commandList_execOnRemote
from .config            import  LOCAL_FILE_DIRECTORY, SSH_CONFIG_VALUES
from .log               import  LOGGER
from .client            import RemoteClient

import  pudb

from .config import (
    SCP_DESTINATION_FOLDER,
    SSH_KEY_FILEPATH,
    SSH_PASSWORD,
    SSH_REMOTE_HOST,
    SSH_USERNAME,
)

Gstr_title = r"""
             _ _
            | | |
 _ __  _   _| | |  ___  ___ _ __
| '_ \| | | | | | / __|/ __| '_ \
| |_) | |_| | | | \__ \ (__| |_) |
| .__/ \__,_|_|_| |___/\___| .__/
| |           ______       | |
|_|          |______|      |_|
"""

Gstr_synopsis = """

    NAME

        pull_scp

    SYNOPSIS

        docker run --rm fnndsc/pl-pull_scp pull_scp                     \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            [--username <username>]                                     \\
            [--password <password>]                                     \\
            [--host <hostname>]                                         \\
            [--sshPubKeyFile <pubKeyFile>]                              \\
            --filepath <filepath>                                       \\
            <outputDir>

    BRIEF EXAMPLE

        * Bare bones execution

            docker run --rm -u $(id -u)                                 \\
                -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing          \\
                fnndsc/pl-pull_scp pull_scp                             \\
                --username johnnyapple                                  \\
                --password 'mysecret'                                   \\
                --host computer.org                                     \\
                --sshPubKeyFile ~/.ssh/id_rsa.pub                       \\
                --filepath /home/johnnyapple/data                       \\
                /outgoing

    DESCRIPTION

        ``pull_scp`` is a *ChRIS fs-type* application that produces data for
        an analysis tree by copying data off a remote host using (recursive)
        ``scp``.

        Of course this assumes that the user executing this plugin has the
        correct login credentials to access the resource. Credentials are
        defined in either:

            * a hard-coded .env file in the repo/container
            * setting appropriate environment variables
            * using plugin CLI arguments

        Other than login credentials, this plugin also needs a ``filepath`` in
        the remote user space. All files and directories rooted in this file
        ``filepath`` are copied into this plugin's ``outputdir``.

    WARNING

        This plugin/app is not considered or purported to be secure! One
        deployment vector has the login credentials contained within an
        `.env` file in cleartext and copied into the container. Deploying
        such a container will expose login credentials! For better security,
        supply login credentials from the CLI or from within environment
        variables:

                export ENVIRONMENT=development
                export SSH_REMOTE_HOST=1.1.1.1
                export SSH_USERNAME=yourname
                export SSH_PASSWORD=yourpassword
                export SSH_KEY_FILEPATH=/usr/local/src/key.pub
                export SCP_DESTINATION_FOLDER=/tmp


    CREDIT

        Most of the innards of this plugin are lightly adapted from the most
        excellent paramiko tutorial of Todd Birchard:

            https://hackersandslackers.com/automate-ssh-scp-python-paramiko

    ARGS

        --filepath <filepath>
        The path in the <hostname>'s filesystem to pull. This is technically
        the only required argument of this plugin. All user specific
        credentials are assumed to be container in the .env file or set in
        environment variables. Note of course that all the credentials can
        be overriden with CLI flags.

        [--username <username>]
        The username in the remote host.

        [--password <password>]
        The <username>'s password to connect to the remote host.

        [--sshPubKeyFile <pubKeyFile>]
        The ssh public key file to use in this session.

        [--host <hostname>]
        The hostname to access.

        [-h] [--help]
        If specified, show help message and exit.

        [--json]
        If specified, show json representation of app and exit.

        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.

        [--savejson <DIR>]
        If specified, save json representation file to DIR and exit.

        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.

        [--version]
        If specified, print version number and exit.
"""


class Pull_scp(ChrisApp):
    """
    This plugin application is used to recursively copy data from a remote host into an analysis root node.
    """
    PACKAGE                 = __package__
    TITLE                   = "A ChRIS plugin FS app that scp's data from a remote host"
    CATEGORY                = 'utility'
    TYPE                    = 'fs'
    ICON                    = ''   # url of an icon image
    MIN_NUMBER_OF_WORKERS   = 1    # Override with the minimum number of workers as int
    MAX_NUMBER_OF_WORKERS   = 1    # Override with the maximum number of workers as int
    MIN_CPU_LIMIT           = 1000 # Override with millicore value as int (1000 millicores == 1 CPU core)
    MIN_MEMORY_LIMIT        = 200  # Override with memory MegaByte (MB) limit as int
    MIN_GPU_LIMIT           = 0    # Override with the minimum number of GPUs as int
    MAX_GPU_LIMIT           = 0    # Override with the maximum number of GPUs as int

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        self.add_argument('--username',
            dest        = 'str_username',
            type        = str,
            optional    = True,
            default     = "",
            help        = 'The username in the remote computer.'
        )
        self.add_argument('--password',
            dest        = 'str_password',
            type        = str,
            optional    = True,
            default     = "",
            help        = "The <username>'s password in the remote computer."
        )
        self.add_argument('--host',
            dest        = 'str_hostname',
            type        = str,
            optional    = True,
            default     = "",
            help        = 'The name of the remote computer.'
        )
        self.add_argument('--sshPubKeyFile',
            dest        = 'str_sshPubKeyFile',
            type        = str,
            optional    = True,
            default     = "",
            help        = 'The ssh public key file to use.'
        )
        self.add_argument('--filepath',
            dest        = 'str_filepath',
            type        = str,
            optional    = False,
            default     = "",
            help        = 'The location in the remote computer to pull.'
        )

    def loginParams_check(self, options):
        """Check the login details. If not specified from CLI args,
           then use details either supplied in the .env file of the
           container itself, or alternatively environment variables.
        """
        global  SSH_USERNAME,       SSH_PASSWORD,       SSH_REMOTE_HOST
        global  SSH_KEY_FILEPATH,   SSH_CONFIG_VALUES
        if len(options.str_username):
            SSH_USERNAME                = options.str_username
        if len(options.str_password):
            SSH_PASSWORD                = options.str_password
        if len(options.str_hostname):
            SSH_REMOTE_HOST             = options.str_hostname
        if len(options.str_sshPubKeyFile):
            SSH_KEY_FILEPATH            = options.str_sshPubKeyFile
        SSH_CONFIG_VALUES               = [
                {"host":        SSH_REMOTE_HOST},
                {"user":        SSH_USERNAME},
                {"password":    SSH_PASSWORD},
                {"ssh":         SSH_KEY_FILEPATH},
                {"path":        SCP_DESTINATION_FOLDER},
        ]

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        self.loginParams_check(options)

        self.client             = RemoteClient(
                                    SSH_REMOTE_HOST,
                                    SSH_USERNAME,
                                    SSH_PASSWORD,
                                    SSH_KEY_FILEPATH,
                                    SCP_DESTINATION_FOLDER,
                                )
        str_remotedirs  : str   = 'find %s -type d' % options.str_filepath
        str_remotesize  : str   = 'du -ksh %s'      % options.str_filepath
        str_remotefiles : str   = 'ls -d %s'        % options.str_filepath
        l_remotefiles   : list  = []
        l_remotesize    : list  = []
        l_remotedirs    : list  = []
        options.verbosity       = int(options.verbosity)
        self.client.localpath   = options.outputdir
        self.client.verbosity   = options.verbosity

        # Intro
        if options.verbosity:
            print(Gstr_title)
            print('Version: %s' % self.get_version())
        if options.verbosity >= 3:
            LOGGER.info('%s' % SSH_CONFIG_VALUES)
            LOGGER.info('remote dirtree: "%s"' % str_remotedirs)
            # Get a list of remote directories...
            l_remotedirs = commandList_execOnRemote(
                self.client,
                [str_remotedirs]
            )

        if options.verbosity >=1 :
            # Determine the recursive pull size on the <str_filepath>...
            l_remotesize = commandList_execOnRemote(
                self.client,
                [str_remotesize],
                False
            )

        # Execute the recursive pull on the remote <str_filepath>...
        l_remotefiles = commandList_execOnRemote(
            self.client,
            [str_remotefiles],
            True
        )
        if len(l_remotefiles[0]['stdout']):
            self.client.bulk_pullObj(l_remotefiles[0]['stdout'])

        if options.verbosity:
            LOGGER.info("Remote contents pulled to %s" % options.outputdir)
            LOGGER.info(
                """(NOTE: if running in a container, and doing a volume mapping,
                            the destination dir name might not match the host dirname!)""")
            process = run(['du', '-ksh',  '%s' % options.outputdir],
                            capture_output  = True,
                            text            = True)
            LOGGER.info('(local): du -ksh %s: %s' % (options.outputdir, process.stdout))

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
