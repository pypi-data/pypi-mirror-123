from os import makedirs
from io import TextIOWrapper
import click
import pprint

from energinetml.core.logger import MetricsLogger

from energinetml.settings import DEFAULT_RELATIV_ARTIFACT_PATH
from energinetml.settings import DEFAULT_RELATIV_LOG_FILENAME
# from click._compat import _default_text_stderr, _default_text_stdout
from click._compat import text_type, string_types
from click._compat import is_bytes
from click._compat import _find_binary_writer
from click.globals import resolve_color_default
from click._compat import should_strip_ansi, strip_ansi, auto_wrap_for_ansi
from click._compat import WIN
# if WIN:
#     from click._winconsole import _get_windows_argv
#     from click._winconsole import _hash_py_argv
#     from click._winconsole import _initial_argv_hash

echo_native_types = string_types + (bytes, bytearray)


def echo_logger(message: str = None):
    """This function is used to "log" local training runs. This function will
    write message to stdout or stderr and append the message to the log file.
    The log file will be uploaded to AML together with the model object
    after the local training script has been completed.

    The function is a modification of the click.utils.echo()

    Args:
        message (str, optional): Your string you want to log. Defaults to None.
    """
    # file handle
    file: TextIOWrapper = open(DEFAULT_RELATIV_LOG_FILENAME, "a")
    color = None

    # TODO: How to make sure the folder exist before running the cmd?
    # Would it make more sense for do this check (and creation) in a different
    # place?
    makedirs(DEFAULT_RELATIV_ARTIFACT_PATH, exist_ok=True)

    # cat ~/.miniconda3/envs/eml/lib/python3.8/site-packages/click/utils.py

    # Convert non bytes/text into the native string type.
    if message is not None and not isinstance(message, echo_native_types):
        message = text_type(message)

    # If there is a message, and we're in Python 3, and the value looks
    # like bytes, we manually need to find the binary stream and write the
    # message in there.  This is done separately so that most stream
    # types will work as you would expect.  Eg: you can write to StringIO
    # for other cases.
    if message and is_bytes(message):
        binary_file = _find_binary_writer(file)
        if binary_file is not None:
            file.flush()
            binary_file.write(message)
            binary_file.flush()
            return

    # ANSI-style support.  If there is no message or we are dealing with
    # bytes nothing is happening.  If we are connected to a file we want
    # to strip colors.  If we are on windows we either wrap the stream
    # to strip the color or we use the colorama support to translate the
    # ansi codes to API calls.
    if message and not is_bytes(message):
        color = resolve_color_default(color)
        if should_strip_ansi(file, color):
            message = strip_ansi(message)
        elif WIN:
            if auto_wrap_for_ansi is not None:
                file = auto_wrap_for_ansi(file)
            elif not color:
                message = strip_ansi(message)

    if message:
        # Print to both the file and console
        print(message)
        file.write(message + "\n")
    file.flush()


class AzureMlLogger(MetricsLogger):
    def __init__(self, run):
        """
        :param azureml.core.Run run:
        """
        self.run = run

    def echo(self, s):
        echo_logger(s)

    def log(self, name, value):
        self.run.log(name, value)
        self.echo('LOG: %s = %s' % (name, value))

    def tag(self, key, value):
        self.run.tag(key, value)
        self.echo('TAG: %s = %s' % (key, value))

    def table(self, name, dict_of_lists, echo=True):
        list_of_dicts = [dict(zip(dict_of_lists, t))
                         for t in zip(*dict_of_lists.values())]

        for d in list_of_dicts:
            self.run.log_table(name, d)

        if echo:
            # TODO print actual table
            self.echo('%s:' % name)
            self.echo(pprint.PrettyPrinter(indent=4).pformat(dict_of_lists))

    def dataframe(self, name, df):
        df = df.reset_index()
        self.table(name, df.to_dict(orient='list'), echo=False)
        self.echo(df.to_string())
