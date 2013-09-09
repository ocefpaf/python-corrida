# -*- coding: utf-8 -*-
#
# gpx_to_json.py
#
# purpose:  Convert the first track of a gpx file to geojson
# author:   Filipe P. A. Fernandes
# e-mail:   ocefpaf@gmail
# web:      http://ocefpaf.github.io/
# created:  08-Sep-2013
# modified: Mon 09 Sep 2013 11:14:16 AM BRT
#
# obs:  Assumes only one track and that track is the only desired feature in
#  the file!
#
# Direct command line alternative:
# ogr2ogr -f "GeoJSON" 2013-02-27-Running.json 2013-02-03-Running.gpx tracks
# However, the scrip below performs some clean-ups that make the GeoJSON reable
# by github.
#

__doc__ = """
Convert gpx tracks to GeoJSON.

Usage:
    gpx_to_json FILE [--output=fout]
    gpx_to_json (-h | --help | --version)

Examples:
    gpx_to_json 2013-02-03-Running.gpx
    gpx_to_json 2013-02-03-Running.gpx --output=2013-02-03-Running.geojson

Arguments:
  file      gpx file.

Options:
  --version   Show version.
  ---help     Show this screen.
"""

import os
import json

from osgeo import ogr
from docopt import docopt


driver = ogr.GetDriverByName("GeoJSON")


def convert(fname):
    """Convert GPX to GeoJSON."""
    fname = os.path.abspath(fname)
    data = ogr.Open(fname)
    tracks = data.GetLayer("tracks")
    # NOTE: Assumes only one track per file.
    geojson = tracks.GetFeature(0).ExportToJson()
    parsed = json.loads(geojson)
    # Cleaned-up GeoJSON by extracting just the geometry.
    return parsed['geometry']


def save_geojson(fout, track):
    """Save as save fname with ".geojson" extension."""
    fout = os.path.abspath(fout)
    with open(fout, 'w') as f:
        json.dump(track, f, indent=4, sort_keys=True)
    return None

if __name__ == '__main__':
    args = docopt(__doc__, version='0.1.0')
    fname = args.get('FILE')
    fout = args.get('--output')

    track = convert(fname)
    if fout:
        save_geojson(fout, track)
    else:
        print(json.dumps(track, indent=4, sort_keys=True))
