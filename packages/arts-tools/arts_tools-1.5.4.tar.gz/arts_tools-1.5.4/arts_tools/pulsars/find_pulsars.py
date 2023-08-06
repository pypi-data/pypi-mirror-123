#!/usr/bin/env python3

import sys

import argparse
import warnings

import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.visualization.wcsaxes import SphericalCircle
from psrqpy import QueryATNF

from arts_tools import tools
from arts_tools.constants import CB_HPBW, REF_FREQ, NCB


def get_half_power_width(freq):
    """
    Calculate compound beam half-power width, assuming linear scaling with frequency

    :param Quantity freq: Frequency
    :return: half-power width (Quantity)
    """
    scaling = freq / REF_FREQ
    hpbw = CB_HPBW * scaling
    return hpbw.to(u.arcmin)


def make_plot(cb_coord, psr_coord, hpbw):
    """
    Create a plot of the CB pattern with pulsar locations

    :param list cb_coord: List of SkyCoord objects with CB pointings
    :param list psr_coord: List of (name, SkyCoord) tuples with pulsar names and positions
    :param Quantity hpbw: half-power beam width of the CBs
    """
    fig, ax = plt.subplots()
    # CB positions
    for cb_idx, cb_pos in enumerate(cb_coord):
        ax.text(cb_pos.ra.deg, cb_pos.dec.deg, f'{cb_idx:02d}', ha='center', va='center', alpha=.5)
        patch = SphericalCircle((cb_pos.ra, cb_pos.dec), hpbw, ec='k', fc='none', ls='-', alpha=.5)
        ax.add_patch(patch)
    # pulsar positions
    for name, coord in psr_coord:
        ax.plot(coord.ra.deg, coord.dec.deg, marker='o', color='red')
        ax.text(coord.ra.deg + .1, coord.dec.deg, name, va='center', ha='left')
    plt.show()


def main():
    # default parameters to query
    params = ["NAME", "BNAME", "RAJ", "DECJ", "DM", "P0", "S1400"]

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description="For a given pointing, determine which pulsars are in the field and "
                                                 "in which compound beam they are.")

    parser.add_argument("--ra", required=True, help="Right Ascension of pointing in hh:mm:ss.s format")
    parser.add_argument("--dec", required=True, help="Declination of pointing in dd:mm:ss.s format")
    parser.add_argument("--freq", type=float, default=1370,
                        help="Observing frequency (MHz), used to determine size of compound beams. "
                             "If max_dist is used, the frequency is only used for plotting the CBs."
                             "(Default: %(default)s)")
    parser.add_argument("--max_dist", type=float, help="Maximum distance from CB center (arcmin) to be considered "
                                                       "in the CB. (Default: twice half-power width)")
    parser.add_argument("--condition", type=str, help="Search condition when querying psrcat, e.g. "
                                                      "'S1400 > 1'")
    parser.add_argument("--more_info", action="store_true", help="Add pulsar parameters to output")
    parser.add_argument("--params", nargs="+", default=params,
                        help=f"Space-separated list of pulsar parameters to show "
                             f"when more_info=True. (Default: {' '.join(params)})")
    parser.add_argument("--plot", action="store_true", help="Plot CB pattern with pulsar locations")

    # print help if no arguments are given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    # set max dist if not given
    half_power_width = get_half_power_width(args.freq * u.MHz)
    if args.max_dist is None:
        args.max_dist = 2 * half_power_width.to(u.arcmin).value

    # query ATNF for pulsars in a 4x4 degree FoV, which covers more than the entire Apertif FoV
    bound = [args.ra, args.dec, 4]
    # params to query should always include NAME, RAJ and DECJ
    query_params = args.params[:]
    for key in ["NAME", "RAJ", "DECJ"]:
        if key not in query_params:
            query_params.append(key)
    print("Querying ATNF")
    # for some reason the query gives a RuntimeWarning, suppress it
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        results = QueryATNF(params=query_params, circular_boundary=bound, condition=args.condition)

    if len(results) == 0:
        print("No pulsars found")
        sys.exit()

    # find the pointing of each CB
    pointing = SkyCoord(args.ra, args.dec, unit=(u.hourangle, u.deg))
    cb_pointings = []
    for cb in range(NCB):
        cb_ra, cb_dec = tools.cb_index_to_pointing(cb, pointing.ra, pointing.dec)
        cb_pointings.append(SkyCoord(cb_ra, cb_dec))

    # check the closest CB for each pulsar
    output = []
    pulsar_coords = []
    pulsar_found = False
    print("Locating pulsars in Apertif Compound Beams")
    for psr in results.table:
        psr_coord = SkyCoord(psr["RAJ"], psr["DECJ"], unit=(u.hourangle, u.deg))
        # get separation from each CB and find minimum
        separations = [psr_coord.separation(beam).to(u.arcmin).value for beam in cb_pointings]
        # index of lowest separation is best CB
        best_cb = np.argmin(separations)
        # check the separation itself
        sep = separations[best_cb]
        # if too far away, skip this pulsar
        # sep must be in acrmin here
        if sep > args.max_dist:
            continue
        # a good pulsar was found
        pulsar_found = True
        # store info
        output.append([best_cb, sep, psr])
        pulsar_coords.append([psr["NAME"], psr_coord])

    if not pulsar_found:
        print("No pulsars found")
        sys.exit()

    # print info sorted by CB
    output = np.array(output)
    order = np.argsort(output[:, 0])

    print("Pulsars found:")
    for cb, sep, psr in output[order]:
        print(f"PSR {psr['NAME']} in CB{cb:02d}, separation from CB centre: {sep:.2f}\"")
        if args.more_info:
            for p in args.params:
                # get value and unit
                value = psr[p]
                unit = psr.columns[p].unit
                dtype = psr.columns[p].dtype
                # format according to dtype
                if dtype == np.float:
                    formatted_value = f" {p} = {value:.2f}"
                else:
                    formatted_value = f" {p} = {value}"
                # add unit
                if unit is not None:
                    formatted_value += f" {unit}"
                # add newline
                print(formatted_value)
            print()

    if args.plot:
        make_plot(cb_pointings, pulsar_coords, half_power_width)
