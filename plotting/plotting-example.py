# -*- coding: utf-8 -*-
#
# plotting-example.py
#
# purpose:  Manually plotting over "Open Street Map" image.
# author:   Filipe P. A. Fernandes
# e-mail:   ocefpaf@gmail
# web:      http://ocefpaf.tiddlyspot.com/
# created:  13-Feb-2013
# modified: Mon 09 Sep 2013 11:27:10 AM BRT
#
# obs: http://www.openstreetmap.org/export?
#      bbox=-46.7437,-23.5728,-46.71,-23.5496#"
#


from __future__ import division

import gpxpy
import gpxpy.gpx
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap


def make_map(llcrnrlon, urcrnrlon, llcrnrlat, urcrnrlat, image):
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


def read_gpx(fname):
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
    lon, lat, elv = read_gpx(fname='GPX/2013-02-06-Running.gpx')
    llcrnrlon, urcrnrlon = -46.7437, -46.7100
    llcrnrlat, urcrnrlat = -23.5728, -23.5496
    fig, ax, m = make_map(llcrnrlon=llcrnrlon, urcrnrlon=urcrnrlon,
                          llcrnrlat=llcrnrlat, urcrnrlat=urcrnrlat,
                          image="basemap/openstreetmap.png")

    dx, dy = 0.008, 0.004
    parallels = np.arange(llcrnrlat, urcrnrlat + dy, dy)
    meridians = np.arange(llcrnrlon, urcrnrlon + dx, dx)
    m.drawparallels(parallels, labels=[1, 0, 0, 0])
    m.drawmeridians(meridians, labels=[0, 0, 0, 1])

    m.plot(lon, lat, 'k.', latlon=True, zorder=2)
    plt.show()
