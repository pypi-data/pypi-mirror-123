"""
Collection of general helper functions.
"""

from subprocess import run, CalledProcessError
import sys
import logging


def download_via_http_link(http_link, out_fn=None):
    """
    Given a http link, this function downloads content from the link
    calling wget in a separate process and optionally downloads to a specified location.
    If no location is specified, it will just download to the current directory.
    @param http_link: link to download from
    @param out_fn: output file name
    @return:
    """
    params = ['wget', f"{http_link}", '-O', f"{out_fn}"] if out_fn else ['wget', f"{http_link}"]
    try:
        run(params,
            stdout=sys.stdout,
            stderr=sys.stderr,
            check=True)
    except CalledProcessError as ex:
        print(f"filter-fasta.py  returned with exit code \
                            {ex.returncode}", file=sys.stderr)
        exit(ex.returncode)


def is_gz_file(filepath):
    """
    Hacky test for the magic number in the 2 first bytes of the file to determine if its gzipped.
    @param filepath:
    @return:
    """
    with open(filepath, 'rb') as test_f:
        return test_f.read(2) == b'\x1f\x8b'


def create_stdout_handler(level=logging.DEBUG):
    """
    Creates a logger handler that writes to stdout.
    Just nicer than just printing to std out, since it includes time stamps
    @return:
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    return handler


def create_stdout_logger(level=logging.DEBUG):
    """
    Creates a logger that writes to stdout.
    Just nicer than just printing to std out, since it includes time stamps
    @return:
    """
    my_logger = logging.getLogger()
    my_logger.setLevel(logging.DEBUG)
    my_logger.addHandler(create_stdout_handler(level))
    return my_logger


def compress(input_fn, output_fn=None):
    """
    Compresses the input file using gzip and remove the original file afterwards.
    If the optional output filename is specified the input file is kept and the compressed
    file is written to a newly created file with the given output filename.
    :param input_fn: File to be compressed
    :param output_fn: file name of the output file to be created
    :return:
    """
    try:
        if output_fn is None:
            run(['gzip', input_fn],
                stdout=sys.stdout,
                stderr=sys.stderr,
                check=True)
        else:
            run(['gzip -c', input_fn],
                stdout=output_fn,
                stderr=sys.stderr,
                check=True)

    except CalledProcessError as ex:
        print(f"gzip returned with exit code \
                            {ex.returncode}", file=sys.stderr)
        exit(ex.returncode)