"""Shell subprocesses.

Features an ANSI shell colors and an extended
wrapper for the :py:func:`subprocess.run` method.
"""


import os
import getpass
import subprocess
import logging


logger = logging.getLogger()


class AnsiColor:
    """A selection of shell ansi color strings.

    Insert these values into strings to (de-)colorize shell outputs in a terminal.

    See also: https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
    """
    reset       = "\033[0m"
    black       = "\033[0;30m"
    dark_gray   = "\033[1;30m"
    red         = "\033[0;31m"
    light_red   = "\033[1;31m"
    green       = "\033[0;32m"
    light_green = "\033[1;32m"
    orange      = "\033[0;33m"
    yellow      = "\033[1;33m"
    blue        = "\033[0;34m"
    light_blue  = "\033[1;34m"
    purple      = "\033[0;35m"
    light_purple = "\033[1;35m"
    cyan        = "\033[0;36m"
    light_cyan  = "\033[1;36m"
    light_gray  = "\033[0;37m"
    white       = "\033[1;37m"


def print_colored(text, color, reset = True):
    """Print text to a console with ansi coloring.

    Print a string, but add an ANSI color sequence.

    Args:
        text (str): A text to send to print.
        color (str): An ansi color to decorate `text` with.
        reset (bool): Clear decoration at the end of `text`.
    
    .. exec_code::
        :caption: Example code:
        :caption_output: Result:

        import miscset
        miscset.sh.print_colored("Hello, world!", miscset.sh.AnsiColor.cyan)
    
    """
    text = color + text
    if reset:
        text += AnsiColor.reset
    print(text)


def run(cmd, remote = None, user = None, piped = True, env = None):
    """Run a (series of) shell command(s) as user at a host.

    Wraps the `subprocess.run` method by adding features like:

    - send command as standard input to a runner, which is either
        - the local shell `bash -s` of the current user
        - the local shell using a different user with `sudo -u <user>`, or
        - the remote shell using a specified user login at a host via `ssh <user>@<host>`
    - supply environment paths exported in the shell prior to executing the command
    - return error code, stdout, stderr to a logger from the `logging` module as debug message

    Args:
        cmd (str): A string used as shell command.
        remote (str): A name of a remote server, if given ssh is invoked.
        user (str): A user name to connect with ssh to a `remote` server or
            switch to using sudo for localhost.
        piped (bool): Enable using `bash -s` to pipe commands to shell.
        env (str): Folder paths to use and export in PATH shell variable.

    Returns:
        :py:class:`subprocess.CompletedProcess`: An object holding args, returncode and stdout/stderr values
            from the executed subprocess.

    .. exec_code::
            :caption: Example code:
            :caption_output: Result:

            import miscset
            print(miscset.sh.run("uname").stdout)

    """
    if env is None:
        env = []
    if remote in ["localhost", "127.0.0.1"]:
        remote = None
    if remote:
        runner = ["ssh"]
        if user:
            runner += ["{}@{}".format(user, remote)]
        else:
            runner += [remote]
        if piped:
            runner += ["\"bash -s\""]
        else:
            runner += ["\"{}\"".format(cmd)]
        if len(env):
            env = ":".join(env)
            cmd = "export PATH=\"{}:$PATH\";".format(env) + cmd
    elif user and user != getpass.getuser():
        runner = ["sudo", "-u", user]
        if piped:
            runner += ["bash -s"]
        else:
            # this case failed,
            # since sudo would not understand the string
            # "id -u -n; pwd"
            # as a command unlike ssh?
            runner += ["\"{}\"".format(cmd)]
    else:
        if piped:
            runner = ["bash -s"]
        else:
            runner = [cmd]
    pipe_input = None
    if piped:
        pipe_input = cmd
    if remote and len(env):
        logger.debug("shell paths are {}".format(env))
    logger.debug("shell stdin is {}".format(pipe_input))
    logger.debug("shell runner is {}".format(runner))
    run = subprocess.run(
        " ".join(runner),
        input = pipe_input,
        text = True,
        universal_newlines = True,
        capture_output = True,
        bufsize = 0,
        shell = True)
    def prettify(std):
        std = std.split(os.linesep)
        std = [ line for line in std if len(line) ]
        if len(std):
            std = [""] + std
        std = os.linesep.join(std)
        return std
    logger.debug("shell stdout is {}".format(prettify(run.stdout)))
    logger.debug("shell stderr is {}".format(prettify(run.stderr)))
    logger.debug("shell return code is {}".format(run.returncode))
    return run

