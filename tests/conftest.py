import io
import os
import sys
import traceback
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from subprocess import CalledProcessError
from contextlib import redirect_stdout, redirect_stderr

import pytest

from installed.cli.main import start


@dataclass
class MainRunResult:
    stdout: bytes
    stderr: bytes
    returncode: int
    command: List[str]

    def check_returncode(self):
        if self.returncode != 0:
            raise CalledProcessError(self.returncode, self.command)

@pytest.fixture
def main_runner():
    def runner_function(arguments: List[str], env: Optional[Dict[str, str]] = None, **kwargs: Any):
        old_excepthook = sys.excepthook
        old_argv = sys.argv
        old_environ = os.environ
        old_exit = sys.exit

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
                start()
            except LocalError:
                returncode = 1
            except Exception as e:
                returncode = 1
                sys.excepthook(type(e), e, e.__traceback__)
                #buffer = io.StringIO()
                #with redirect_stderr(buffer):
                #    sys.excepthook(type(e), e, e.__traceback__)
                #traceback_string = buffer.getvalue()
                #if sys.platform.lower() in ('win32',):
                #    #traceback_string = traceback_string.replace(os.linesep, '\n')
                #    traceback_string = traceback_string.replace('\n', os.linesep)
                #print(traceback_string, file=sys.stderr, end='')

            finally:
                if sys.platform.lower() in ('win32',):
                    stdout = stdout.replace('\n', os.linesep)
                    stderr = stderr.replace('\n', os.linesep)
                result = MainRunResult(command=arguments, stdout=str.encode(stdout_buffer.getvalue()), stderr=str.encode(stderr_buffer.getvalue()), returncode=returncode)

        sys.excepthook = old_excepthook
        sys.argv = old_argv
        os.environ = old_environ
        sys.exit = old_exit

        return result

    return runner_function
