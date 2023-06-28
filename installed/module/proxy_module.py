import sys
import logging

from installed.module.context_manager import pip_context
from installed.module.runner import run_python
from installed.module.empty_logger import EmptyLogger
from installed.common_utils.convert_options import convert_options


class ProxyModule(sys.modules[__name__].__class__):
    def __call__(self, *packages_names, logger=logging, runner=run_python, catch_output=False, where=None, **options):
        if logger is None:
            logger = EmptyLogger()
        options = convert_options(options)
        return pip_context(packages_names, options, logger, runner, catch_output, where)
