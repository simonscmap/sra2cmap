#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@email.arizona.edu>
Date   : 2019-02-27
Purpose: Convert SRA metadata to CMAP import
"""

import argparse
import dateparser
import csv
import numpy as np
import os
import re
import sys
from collections import OrderedDict
from datetime import datetime
from openpyxl import Workbook


# --------------------------------------------------
def get_args():
    """get command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Convert SRA metadata to CMAP import',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('sra', metavar='FILE', help='SRA metadata', nargs='+')

    parser.add_argument(
        '-d',
        '--delimiter',
        help='Field delimiter',
        metavar='str',
        type=str,
        default='\t')

    parser.add_argument(
        '-o',
        '--outdir',
        help='Output directory',
        metavar='str',
        type=str,
        default='export')

    return parser.parse_args()


# --------------------------------------------------
def warn(msg):
    """Print a message to STDERR"""
    print(msg, file=sys.stderr)


# --------------------------------------------------
def die(msg='Something bad happened'):
    """warn() and exit with error"""
    warn(msg)
    sys.exit(1)


# --------------------------------------------------
def format_record(rec):
    """Format the required fields: time, lat, lon, depth"""

    for fld in ['time', 'collection_date']:
        col_date = rec.get(fld)
        if col_date:
            dt = dateparser.parse(col_date)
            rec['time'] = dt.isoformat()

    # Combined e.g., 37.8305 S 41.1248 W
    # TODO: Handle other formats, e.g., HMS
    lat_lon = rec.get('lat_lon')
    if lat_lon:
        re1 = r'(\d+(?:\.\d+)?)\s*([NS])?(?:[,\s])(\d+(?:\.\d+)?)\s*([EW])?'
        match = re.search(re1, lat_lon)
        if match:
            lat, lat_dir, lon, lon_dir = match.groups()
            lat = float(lat)
            lon = float(lon)

            if lat_dir and lat_dir == 'S':
                lat *= -1

            if lon_dir and lon_dir == 'W':
                lon *= -1

            rec['lat'] = lat
            rec['lon'] = lon

    # TODO: verify that individual lat/lon fields are in proper format

    # Handles removing any non-numerical data, e.g., "9m"
    depth = rec.get('depth') or rec.get('sample_depth')
    if depth:
        match = re.search(r'(\d+(\.\d+)?)', depth)
        if match:
            rec['depth'] = match.group(1)

    return rec


# --------------------------------------------------
def normalize(s):
    """
    Make identifiers the same (snake_case_all_lower_case), e.g.:

    BioSample => bio_sample
    DATASTORE_filetype => datastore_filetype
    SRA_Study => sra_study
    """

    caps_under_re = re.compile(r'([A-Z]+)(?=[_])')
    s = caps_under_re.sub(lambda x: x.group(1).lower(), s)

    if '_' in s:
        s = '_'.join(map(str.lower, s.split('_')))
    else:
        camel_to_space = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')
        s = camel_to_space.sub(r'_\1', s).lower()

    return s


# --------------------------------------------------
def main():
    """Make a jazz noise here"""
    args = get_args()
    out_dir = args.outdir

    if not os.path.isdir(out_dir): os.makedirs(out_dir)

    for i, file in enumerate(args.sra, start=1):
        if not os.path.isfile(file):
            warn('"{}" is not a file'.format(file))
            continue

        basename = os.path.basename(file)
        root, ext = os.path.splitext(basename)

        print('{:3}: {}'.format(i, basename))

        out_file = os.path.join(out_dir, root + '.xlsx')
        wb = Workbook()

        req_flds = ['time', 'lat', 'lon', 'depth']
        with open(file) as fh:
            ws = wb.active
            reader = csv.DictReader(fh, delimiter=args.delimiter)
            flds = req_flds + reader.fieldnames
            norm2fld = OrderedDict(map(lambda s: (normalize(s), s), flds))
            ordered_flds = list(norm2fld.keys())
            ws.append(ordered_flds)

            for row in reader:
                clean = format_record(row)
                if all([fld in row for fld in req_flds]):
                    ws.append([clean[norm2fld[fld]] for fld in ordered_flds])

        wb.save(out_file)

    print('Done, see output in "{}".'.format(out_dir))


# --------------------------------------------------
if __name__ == '__main__':
    main()
