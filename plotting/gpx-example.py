# -*- coding: utf-8 -*-
#
# gpx-example.py
#
# purpose:
# author:   Filipe P. A. Fernandes
# e-mail:   ocefpaf@gmail
# web:      http://ocefpaf.tiddlyspot.com/
# created:  13-Feb-2013
# modified: Mon 18 Feb 2013 11:13:54 AM BRT
#
# obs:
#

"http://www.openstreetmap.org/export?bbox=-46.7437,-23.5728,-46.71,-23.5496#"

from __future__ import division

import gpxpy
import gpxpy.gpx
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap


def make_map(llcrnrlon=-46.7437, urcrnrlon=-46.71,
             llcrnrlat=-23.5728, urcrnrlat=-23.5496, image="map.png"):

    fig, ax = plt.subplots()
    m = Basemap(llcrnrlon=llcrnrlon, urcrnrlon=urcrnrlon,
                llcrnrlat=llcrnrlat, urcrnrlat=urcrnrlat,
                resolution='c', projection='merc',
                lon_0=(urcrnrlon + llcrnrlon) / 2,
                lat_0=(urcrnrlat + llcrnrlat) / 2,
                lat_ts=-23.5)

    m.ax = ax
    m.imshow(plt.imread(image), origin='upper', zorder=1)
    return fig, ax, m


def read_gpx(fname='2013-02-06-Running.gpx'):
    gpx_file = open(fname, 'r')
    gpx = gpxpy.parse(gpx_file)
    lon, lat, elv = [], [], []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lon.append(point.longitude)
                lat.append(point.latitude)
                elv.append(point.elevation)

    lon, lat, elv = map(np.array, (lon, lat, elv))
    return lon, lat, elv

if __name__ == '__main__':
    lon, lat, elv = read_gpx(fname='2013-02-06-Running.gpx')
    llcrnrlon = -46.7437
    urcrnrlon = -46.7100
    llcrnrlat = -23.5728
    urcrnrlat = -23.5496
    fig, ax, m = make_map(llcrnrlon=llcrnrlon, urcrnrlon=urcrnrlon,
                          llcrnrlat=llcrnrlat, urcrnrlat=urcrnrlat,
                          image="map-usp.png")

    parallels = np.arange(llcrnrlat, urcrnrlat, 0.004)
    meridians = np.arange(llcrnrlon, urcrnrlon, 0.008)
    kw = dict()
    m.drawparallels(parallels, labels=[1, 0, 0, 1], **kw)
    m.drawmeridians(meridians, labels=[1, 1, 0, 1], **kw)

    m.plot(lon, lat, 'k.', latlon=True, zorder=2)
    plt.show()
