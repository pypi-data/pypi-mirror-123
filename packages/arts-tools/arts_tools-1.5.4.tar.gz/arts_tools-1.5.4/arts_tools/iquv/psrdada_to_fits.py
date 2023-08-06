#!/usr/bin/env python3

import sys
import os
import argparse
import logging
from multiprocessing import Process
from time import sleep

import numpy as np

from arts_tools.constants import NTAB, NSB, SB_TABLE

# check psrdada import as psrdada-python is not an explicit requirement in setup.py
try:
    import psrdada
except ImportError:
    raise ImportError("Cannot import psrdada; Is psrdada-python installed?")

#: Number of polarizations
NPOL = 4
#: Number of channels
NCHAN = 1536
#: Number of samples per PSRDADA page
NSAMP = 12500


def get_psrdada_header(fname):
    """
    Read header raw PSRDADA file

    :param str fname: Path to PSRDADA file
    :return: header (dict)
    """
    # load a typical amount of bytes from the file and look for header size keyword
    nbyte = 1
    raw_header = ''
    with open(fname, 'r') as f:
        while True:
            raw_header = raw_header + f.read(nbyte)
            header = [line.strip().split(maxsplit=1) for line in raw_header.split('\n')]
            header = np.array(header)
            try:
                key_index = np.where(header == 'HDR_SIZE')[0]
                hdr_size = header[key_index, 1][0].astype(int)
            except (IndexError, ValueError):
                if nbyte > 1e6:
                    logging.error(f"Key HDR_SIZE not found in first MB of PSRDADA file {fname}")
                    sys.exit(1)
                nbyte += 4096
            else:
                break
        # load the full header with known size
        f.seek(0)
        header = f.read(hdr_size)
        # convert to dict, skipping empty lines and zero padding at the end
        header = dict([line.strip().split(maxsplit=1) for line in header.split('\n') if line][:-1])
    return header


def read_psrdada_to_buffer(files, header, key, dadafits):
    """
    Read PSRDADA files into a memory buffer

    :param list files: Files to read into memory buffer
    :param dict header: PSRDADA header
    :param str key: PSRDADA shared memory key
    :param Process dadafits: Handle to dadafits process
    """
    # convert key to hexadecimal
    hexkey = int(key, 16)

    # connect to the memory buffer
    writer = psrdada.Writer()
    writer.connect(hexkey)

    # write header
    writer.setHeader(header)

    # sort input files
    files.sort()

    # loop over files and read them into header
    for i, fname in enumerate(files):
        with open(fname, 'rb') as f:
            # skip header
            f.seek(int(header['HDR_SIZE']))
            # read data page by page
            while True:
                # check if dadafits is still alive to read the data we are about to write
                if not dadafits.is_alive():
                    # not calling writer.disconnect here, as it hangs forever. Unclear why
                    # raise an error here, as it is caught and logged by the main programme
                    raise ChildProcessError("dadafits no longer running; not writing new data")

                data = np.fromfile(f, count=int(header['RESOLUTION']), dtype='uint8')
                # if at end of file, break loop
                if len(data) == 0:
                    break
                # write page into buffer
                page = np.asarray(writer.getNextPage())
                page[:] = data[:]
                # mark the buffer as filled
                writer.markFilled()

    # done, mark end of data, then disconnect
    writer.getNextPage()
    writer.markEndOfData()
    writer.disconnect()


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description=f"Convert raw IQUV data to PSRFITS.\n"
                                                 f"The output can either be one file for each "
                                                 f"of the {NTAB} tied-array beams (TABs),\nor one "
                                                 f"file for each user-specified synthesized beam (SB) "
                                                 f"between 0 and {NSB}.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--tab', action='store_true', help="Create TABs instead of SBs")
    group.add_argument('--sb', type=int, nargs='*', help="Space-separated list of SBs to create")

    parser.add_argument('--output_dir', required=True, help="Output directory")
    parser.add_argument('--key', default='dada', help="4-digit hexadecimal Key to use for PSRDADA shared "
                                                      "memory buffer (Default: %(default)s)")
    parser.add_argument('--templates', help="Path to folder with FITS templates "
                                            "(Default: use templates provided with package)")
    parser.add_argument('--sbtable', help="Path to SB table "
                                          "(Default: use SB table provided with package)")
    parser.add_argument('--verbose', '-v', action='store_true', help="Increase verbosity")

    parser.add_argument('raw_files', nargs='+', help="Path to input PSRDADA file(s) belonging to one observation. "
                                                     "If multiple files are given, they are sorted by filename "
                                                     "before processing")

    # print help if no arguments are given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    # set log verbosity
    if args.verbose:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging_level, stream=sys.stderr)

    logging.debug(f"Arguments: {args}")

    # verify the input files exist
    for fname in args.raw_files:
        if not os.path.isfile(fname):
            logging.error(f"Input file does not exist: {fname}")
            sys.exit(1)

    # set FITS templates dir and SB table dir
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    if args.templates is None:
        args.templates = os.path.join(root_dir, 'static', 'fits_templates')
        logging.debug(f"Setting FITS templates directory to {args.templates}")
    if args.sbtable is None:
        args.sbtable = os.path.join(root_dir, SB_TABLE)
        logging.debug(f"Setting SB table to {args.sbtable}")

    # set SB command
    if args.tab:
        sb_cmd = ""
    else:
        # check if SB range is valid
        if (np.any(args.sb) > NSB) or np.any(args.sb) < 0:
            logging.error(f"Invalid SB index given, allowed values are 0 to {NSB}")
            sys.exit(1)
        sb_cmd = f"-S {args.sbtable} -s " + ','.join(map(str, args.sb))

    # create output directory
    if os.path.isdir(args.output_dir):
        logging.warning(f"Output directory already exists: {args.output_dir}")
    try:
        os.makedirs(args.output_dir, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create output directory: {e}")
        sys.exit(1)

    # get PSRDADA header from first file
    header = get_psrdada_header(args.raw_files[0])

    # create memory buffer (single page, as processing is slower than reading data anyway)
    buffer_size = NTAB * NCHAN * NSAMP * NPOL
    cmd = f"dada_db -a {header['HDR_SIZE']} -b {buffer_size} -n 1 -k {args.key} -w 2>/dev/null"
    logging.debug(f"dada_db command: {cmd}")
    memory_buffer = Process(target=os.system, args=(cmd, ), name='dada_db')
    logging.info(f"Creating PSRDADA memory buffer of size {buffer_size / 1e9} GB")
    memory_buffer.start()
    sleep(1)

    # if the memory buffer is not alive, something failed (probably key that was already in use)
    if not memory_buffer.is_alive():
        logging.error(f"Failed to set up memory buffer, perhaps PSRDADA key is already in use? "
                      f"Run \"dada_db -d -k {args.key}\" to remove it (But be careful not to remove "
                      f"buffers used by observations when running this script on any of arts001 - arts040)")
        sys.exit(1)

    # run FITS writer
    cmd = f"dadafits -k {args.key} -l /dev/null -t {args.templates} -d {args.output_dir} {sb_cmd}"
    logging.debug(f"dadafits command: {cmd}")
    dadafits = Process(target=os.system, args=(cmd, ), name='dadafits')
    logging.info(f"Starting dadafits")
    dadafits.start()
    sleep(1)

    # read data into buffer
    try:
        read_psrdada_to_buffer(args.raw_files, header, args.key, dadafits)
    except Exception as e:
        logging.error(f"Exception in writing data to memory buffer: {type(e).__name__}: {e}")
        # remove the running Processes
        dadafits.terminate()
        # sometimes terminating the buffer Process does not actually remove the buffer, so
        # remove it explicitly first
        cmd = f"dada_db -d -k {args.key} >/dev/null 2>&1"
        os.system(cmd)
        memory_buffer.terminate()
        sys.exit(1)

    # when done reading data into buffer, wait until dadafits exits
    logging.info("Waiting for dadafits to finish")
    dadafits.join()
    logging.info("dadafits finished")

    # remove the memory buffer
    logging.info("Removing PSRDADA memory buffer")
    # sometimes terminating the buffer Process does not actually remove the buffer, so
    # remove it explicitly first
    cmd = f"dada_db -d -k {args.key} >/dev/null 2>&1"
    os.system(cmd)
    memory_buffer.terminate()

    logging.info("Done")
