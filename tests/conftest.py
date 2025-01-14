import io
import os
import sys
import traceback
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from subprocess import CalledProcessError
from contextlib import redirect_stdout, redirect_stderr

import pytest

from instld.cli.main import main


@dataclass
class MainRunResult:
    stdout: bytes
    stderr: bytes
    before_stderr: bytes
    returncode: int
    command: List[str]

    def check_returncode(self):
        if self.returncode != 0:
            raise CalledProcessError(self.returncode, self.command)

@pytest.fixture
def main_runner():
    def runner_function(arguments: List[str], env: Optional[Dict[str, str]] = None, universal_newlines: Optional[bool] = None, **kwargs: Any):
        old_excepthook = sys.excepthook
        old_argv = sys.argv
        old_environ = os.environ
        old_exit = sys.exit
        old_env = os.environ

        if env is not None:
            os.environ = env

        sys.argv = arguments

        class LocalError(Exception): pass
        def exit_handler(number): raise LocalError
        sys.exit = exit_handler

        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        returncode = 0
        with redirect_stdout(stdout_buffer) as stdout, redirect_stderr(stderr_buffer) as stderr:
            try:
                main()
                stdout = stdout_buffer.getvalue()
                stderr = stderr_buffer.getvalue()
                before_stderr = str.encode(stderr)
            except LocalError:
                returncode = 1
                stdout = stdout_buffer.getvalue()
                stderr = stderr_buffer.getvalue()
                before_stderr = str.encode(stderr)
            except Exception as e:
                returncode = 1
                sys.excepthook(type(e), e, e.__traceback__)
                stdout = stdout_buffer.getvalue()
                stderr = stderr_buffer.getvalue()
                before_stderr = str.encode(stderr)
                if sys.platform.lower() in ('win32',):
                    stdout = stdout.replace('\n', os.linesep).replace('\r\r', '\r')
                    stderr = stderr.replace('\n', os.linesep).replace('\r\r', '\r')
            finally:
                if not (universal_newlines is not None and universal_newlines):
                    stdout = str.encode(stdout)
                    stderr = str.encode(stderr)
                result = MainRunResult(command=arguments, stdout=stdout, stderr=stderr, before_stderr=before_stderr, returncode=returncode)

        sys.excepthook = old_excepthook
        sys.argv = old_argv
        os.environ = old_environ
        sys.exit = old_exit
        os.environ = old_env

        return result

    return runner_function
