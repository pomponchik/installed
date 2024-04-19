![logo](https://raw.githubusercontent.com/pomponchik/instld/main/docs/assets/logo_5.png)

# INSTLD: the simplest package management

[![Downloads](https://static.pepy.tech/badge/instld/month)](https://pepy.tech/project/instld)
[![Downloads](https://static.pepy.tech/badge/instld)](https://pepy.tech/project/instld)
[![codecov](https://codecov.io/gh/pomponchik/instld/graph/badge.svg?token=XuhCNeksjG)](https://codecov.io/gh/pomponchik/instld)
[![Lines of code](https://sloc.xyz/github/pomponchik/instld/?category=code)](https://github.com/boyter/scc/)
[![Hits-of-Code](https://hitsofcode.com/github/pomponchik/instld?branch=main)](https://hitsofcode.com/github/pomponchik/instld/view?branch=main)
[![Tests](https://github.com/pomponchik/instld/actions/workflows/tests_and_coverage.yml/badge.svg)](https://github.com/pomponchik/instld/actions/workflows/tests_and_coverage.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/instld.svg)](https://pypi.python.org/pypi/instld)
[![PyPI version](https://badge.fury.io/py/instld.svg)](https://badge.fury.io/py/instld)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Thanks to this package, it is very easy to manage the lifecycle of packages.

- ⚡ Run your code without installing libraries.
- ⚡ You can use 2 different versions of the same library in the same program.
- ⚡ You can use incompatible libraries in the same project, as well as libraries with incompatible/conflicting dependencies.
- ⚡ It's easy to share written scripts. The script file becomes self-sufficient - the user does not need to install the necessary libraries.
- ⚡ The library does not leave behind "garbage". After the end of the program, no additional files remain in the system.


## Table of contents

- [**Quick start**](#quick-start)
- [**REPL mode**](#repl-mode)
- [**Script launch mode**](#script-launch-mode)
- [**Context manager mode**](#context-manager-mode)
  - [**Installing multiple packages**](#installing-multiple-packages)
  - [**Options**](#options)
  - [**Using an existing virtual environment**](#using-an-existing-virtual-environment)
  - [**Output and logging**](#output-and-logging)
- [**Special comment language**](#special-comment-language)
- [**Using multiple environments**](#using-multiple-environments)
- [**How does it work?**](#how-does-it-work)


## Quick start

Install [it](https://pypi.org/project/instld/):

```bash
pip install instld
```

And use the library in one of three ways: by typing commands via REPL, by running your script through it or by importing a context manager from there.

If you run the script [like this](#script-launch-mode), all dependencies will be automatically installed when the application starts and deleted when it stops:

```bash
instld script.py
```

The [REPL mode](#repl-mode) works in a similar way, you just need to type `instld` in the console to enter it.

You can also call the [context manager](#context-manager-mode) from your code:

```python
import instld

with instld('some_package'):
    import some_module
```

Read more about each method, its capabilities and limitations below.


## REPL mode

REPL mode is the fastest and easiest way to try out other people's libraries for your code. Just type this in your console:

```bash
instld
```

After that you will see a welcome message similar to this:

```
⚡ INSTLD REPL based on
Python 3.11.6 (main, Oct  2 2023, 13:45:54) [Clang 15.0.0 (clang-1500.0.40.1)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>>
```

Enjoy the regular Python [interactive console mode](https://docs.python.org/3/tutorial/interpreter.html#interactive-mode)! Any libraries that you ask for will be installed within the session, and after exiting it, they will be deleted without a trace. You don't need to "clean up" anything after exiting the console.

In this mode, a [special comment language](#special-comment-language) is fully supported.

## Script launch mode

You can use `instld` to run your script from a file. To do this, you need to run a command like this in the console:

```bash
instld script.py
```

The contents of the script will be executed in the same way as if you were running it through the `python script.py` command. If necessary, you can pass additional arguments to the command line, as if you are running a regular Python script. However, if your program has imports of any packages other than the built-in ones, they will be installed automatically. Installed packages are automatically cleaned up when you exit the program, so they don't leave any garbage behind.

In this mode, as in [REPL](#repl-mode), a [special comment language](#special-comment-language) is fully supported.


## Context manager mode

You can also use `instld` to install and use packages in runtime. The context manager `instld` generates a context. While you are inside the context manager, you can import modules using the usual `import` command:

```python
with instld('some_package'):
    import some_module
```

However, there are cases when you need the module to be imported strictly from a given context. In this case, it is better to use the `import_here` method:

```python
with instld('some_package') as context:
    module = context.import_here('some_module')
```

The library provides isolation of various contexts among themselves, so in the second case, the module will be imported strictly from the context that you need.

> ⚠️  Some modules use lazy imports. If such an import happens after exiting the context manager, it will break your program. Please make sure that all the internal components of the libraries used have been initialized before the execution of your code goes out of context.


### Installing multiple packages

You can install several packages by specifying their names separated by commas:

```python
with instld('package_1', 'package_2', 'package_3') as context:
    module_1 = context.import_here('module_1')
    module_2 = context.import_here('module_2')
    module_3 = context.import_here('module_3')
```

In this case, all packages will be installed in one context and you can import them all from there.

You can also create separate contexts for different packages:

```python
with instld('package_1') as context_1:
    with instld('package_2') as context_2:
        with instld('package_3') as context_3:
            module_1 = context_1.import_here('module_1')
            module_2 = context_2.import_here('module_2')
            module_3 = context_3.import_here('module_3')
```

In this case, each package was installed in its own independent context, and we import each module from the context where the corresponding package was installed.

This capability is very powerful. You can place libraries in different contexts that are incompatible with each other. You can also install different versions of the same library in neighboring contexts. Here's how it will work using the [Flask](https://flask.palletsprojects.com/) example:

```python
with instld('flask==2.0.2') as context_1:
    with instld('flask==2.0.0') as context_2:
        flask_1 = context_1.import_here('flask')
        flask_2 = context_2.import_here('flask')

        print(flask_1.__version__)  # 2.0.2
        print(flask_2.__version__)  # 2.0.0
```

> ⚠️  Keep in mind that although inter-thread isolation is used inside the library, working with contexts is not completely thread-safe. You can write code in such a way that two different contexts import different modules in separate threads at the same time. In this case, you may get paradoxical results. Therefore, it is recommended to additionally isolate with mutexes all cases where you import something from contexts in different threads.


## Options

You can use [any options](https://pip.pypa.io/en/stable/cli/pip_install/) available for `pip`. To do this, you need to slightly change the name of the option, replacing the hyphens with underscores, and pass it as an argument to `instld`. Here is an example of how using the `--index-url` option will look like:

```python
with instld('super_test_project==0.0.1', index_url='https://test.pypi.org/simple/'):
    import super_test
```

You cannot use options that tell `pip` where to install libraries.


### Using an existing virtual environment

By default, through the [context manager](#context-manager-mode), packages are installed in a temporary virtual environment, which is deleted after exiting the context. However, if you want to install the package in a permanent environment, there is also a way to do this: use the `where` argument.

```python
with instld('package', where='path/to/the/venv'):
    import package
```

When manually specifying the path to the virtual environment directory, you need to consider several points:

1. The format of the separator differs in different operating systems. For example, in Linux it is `/`, and in Windows it is `\`. To make your code multiplatform, use [`os.path.join`](https://docs.python.org/3/library/os.path.html#os.path.join) to define the path.
2. You need to make sure that the virtual environment that you are passing the path to is created by the same Python interpreter that you use to run your code. Virtual environments created by different interpreters are not compatible with each other. For the same reasons, it is not worth storing virtual environment files in Git.


### Output and logging

By default, you can see the output of the installation progress in the console:

```python
>>> with instld('flask'):
...     import flask
...
Collecting flask
  Using cached Flask-2.3.2-py3-none-any.whl (96 kB)
Collecting click>=8.1.3
  Using cached click-8.1.3-py3-none-any.whl (96 kB)
Collecting importlib-metadata>=3.6.0
  Using cached importlib_metadata-6.6.0-py3-none-any.whl (22 kB)
Collecting Jinja2>=3.1.2
  Using cached Jinja2-3.1.2-py3-none-any.whl (133 kB)
Collecting Werkzeug>=2.3.3
  Using cached Werkzeug-2.3.3-py3-none-any.whl (242 kB)
Collecting itsdangerous>=2.1.2
  Using cached itsdangerous-2.1.2-py3-none-any.whl (15 kB)
Collecting blinker>=1.6.2
  Using cached blinker-1.6.2-py3-none-any.whl (13 kB)
Collecting zipp>=0.5
  Using cached zipp-3.15.0-py3-none-any.whl (6.8 kB)
Collecting MarkupSafe>=2.0
  Using cached MarkupSafe-2.1.2-cp39-cp39-macosx_10_9_universal2.whl (17 kB)
Installing collected packages: zipp, MarkupSafe, Werkzeug, Jinja2, itsdangerous, importlib-metadata, click, blinker, flask
Successfully installed Jinja2-3.1.2 MarkupSafe-2.1.2 Werkzeug-2.3.3 blinker-1.6.2 click-8.1.3 flask-2.3.2 importlib-metadata-6.6.0 itsdangerous-2.1.2 zipp-3.15.0
```

If you don't want to see this output, pass the `catch_output` argument:

```python
>>> with instld('flask', catch_output=True):
...     import flask
...
>>>
```

In case of installation errors, you will get an `instld.errors.InstallingPackageError` exception. From the object of this exception, you can get `stdout` and `stderr` even if you have forbidden the output:

```python
from instld.errors import InstallingPackageError


try:
    with instld('some_wrong_pack', catch_output=True):
        import some_wrong_module
except InstallingPackageError as e:
    print(e.stdout)
    print(e.stderr)
```

Logging is also enabled by default for installing packages. You can see it if you configure logging correctly. In this case:

```python
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
    ]
)

with instld('flask', catch_output=True):
    import flask
```

... the logs will look something like this:

```
2023-05-02 13:47:56,752 [INFO] The beginning of the execution of the command "/Users/pomponchik/Desktop/Projects/magic-action-runner/venv/bin/python3 -m venv /var/folders/54/p5qzzp9j65zckq9kd2k31t9c0000gn/T/tmpiajesk4s/venv".
2023-05-02 13:47:58,993 [INFO] The command "/Users/pomponchik/Desktop/Projects/magic-action-runner/venv/bin/python3 -m venv /var/folders/54/p5qzzp9j65zckq9kd2k31t9c0000gn/T/tmpiajesk4s/venv" has been executed.
2023-05-02 13:47:58,993 [INFO] The beginning of the execution of the command "/Users/pomponchik/Desktop/Projects/magic-action-runner/venv/bin/python3 -m pip install --target=/var/folders/54/p5qzzp9j65zckq9kd2k31t9c0000gn/T/tmpiajesk4s/venv/lib/python3.9/site-packages flask".
2023-05-02 13:48:01,052 [INFO] The command "/Users/pomponchik/Desktop/Projects/magic-action-runner/venv/bin/python3 -m pip install --target=/var/folders/54/p5qzzp9j65zckq9kd2k31t9c0000gn/T/tmpiajesk4s/venv/lib/python3.9/site-packages flask" has been executed.
```

The `INFO` [level](https://docs.python.org/3/library/logging.html#logging-levels) is used by default. For errors - `ERROR`.


## Special comment language

When using script launch or REPL mode, you can specify additional parameters for each import inside your program. To do this, you need to write immediately after it (but always in the same line!) a comment that starts with "instld:", separating key and value pairs with commas.

As example, if the name of the imported module and the package name are different, this code imports the `f` function from the [`fazy`](https://github.com/pomponchik/fazy) library version `0.0.3`:

```python
import f # instld: version 0.0.3, package fazy

print(f('some string'))
```

You can also specify only the version or only the package name in the comment, they do not have to be specified together.


## Using multiple environments

The instld script launch mode and REPL mode provides a unique opportunity to use multiple virtual environments at the same time.

Firstly, you can run scripts in the main virtual environment, and it will work exactly as you expect:

```bash
python3 -m venv venv
source venv/bin/activate
instld script.py
```

When the "import" command is executed in your script, the package will first be searched in the activated virtual environment, and only then downloaded if it is not found there. Note that by default, the activated virtual environment is read-only. That is, it is assumed that you will install all the necessary libraries there before running your script. If you want to install packages in runtime in a specific virtual environment - read about the second method further.

Secondly, you can specify the path to the virtual environment directly [in the comments](#special-comment-language) to a specific import using the `where` directive:

```python
import something  # instld: where path/to/the/venv
```

If the path you specified does not exist when you first run the script, it will be automatically created. Libraries installed in this way are not deleted when the script is stopped, therefore, starting from the second launch, the download is no longer required.

Note that the path to the virtual environment in this case should not contain spaces. In addition, there is no multiplatform way to specify directory paths using a comment. Therefore, it is not recommended to use paths consisting of more than one part.

Since script launch mode uses a context manager to install packages "under the hood", you should also read about the features of installing packages in this way in the [corresponding section](#using-an-existing-virtual-environment).


## How does it work?

This package is essentially a wrapper for `venv` and `pip`.

When entering the context, a temporary folder is created using the [tempfile](https://docs.python.org/3/library/tempfile.html) library. Then it is added to [sys.path](https://docs.python.org/3/library/sys.html#sys.path), and after exiting the context, it is removed from there. To install the package in this particular temporary folder, the `--target` argument is passed to pip, indicating the path to it. Interaction with `pip` and `venv` occurs through [subprocesses](https://docs.python.org/3/library/subprocess.html).

The `import_here` method works by temporarily substituting [sys.path](https://docs.python.org/3/library/sys.html#sys.path) and [sys.modules](https://docs.python.org/3/library/sys.html#sys.modules). This is necessary so that the search for packages takes place only in the necessary directories.
