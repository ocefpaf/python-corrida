# -*- coding: utf-8 -*-
#
# corrida.py
#
# purpose:  Reproduce "corrida.for" results.
# author:   Filipe P. A. Fernandes
# e-mail:   ocefpaf@gmail
# web:      http://ocefpaf.tiddlyspot.com/
# created:  27-May-2013
# modified: Fri 07 Jun 2013 06:38:49 PM BRT
#
# obs:
#

from __future__ import division

import numpy as np
from pandas import DataFrame
from cStringIO import StringIO

# Constants.
encoding = 'UTF-8'
pvm = 0.55 + 0.05 * (np.arange(10) + 1)
phr = 0.63 * pvm + 0.37

x = np.array([100, 120, 150, 200, 300, 400, 500, 600, 667, 800, 1000, 1200,
              1500, 1600, 2000, 3000, 5000, 6000, 7000, 8000, 10000, 12000,
              15000, 18000, 20000, 42195 / 2, 42195])


# Utilities.
def Nint(num):
    return np.int_(np.round(num))


def to_csv(df):
    df.index.name = u'Distância'
    csv = StringIO()
    df.to_csv(csv, encoding=encoding)
    csv.seek(0)
    return [line.strip().decode(encoding=encoding) for line in csv.readlines()]


def write_spreadsheet(fname='corrida.csv', lines=None):
    with open(fname, 'w') as f:
        f.writelines(u'\n'.join(lines).encode(encoding))
    return None


# Functions.
def d2hms(t):
    hh = t // 3600
    mm = t // 60 - hh * 60
    ss = Nint(t - mm * 60 - hh * 3600)
    return "%02i:%02i:%02i" % (hh, mm, ss)


def vo2(t, d):
    a, b, r = -4.60, 0.182258, 0.000104
    s = d / t
    return a + b * s + r * s ** 2


def pvmax(t):
    d, e, f, g, h = 0.8, 0.1894393, -0.012778,  0.2989558, -0.1932605
    return d + e * np.exp(f * t) + g * np.exp(h * t)


def vo2max(v, p):
    return v / p


def _estt(estd, vm):
    estd, vm = np.broadcast_arrays(estd[..., None], vm[None, ...])
    estt = estd / 50
    dt = estt / 2
    aeps = 9999
    while aeps > 1e-6:
        v1, p1 = vo2(estt, estd),  pvmax(estt)
        vm1 = vo2max(v1, p1)
        eps = vm1 - vm
        aeps = np.abs(eps).min()
        mask = eps > 1e-6  # Increase estt.
        estt[mask] += dt[mask]
        mask = eps < -1e-6  # Decrease estt.
        estt[mask] -= dt[mask]
        dt /= 2
    return estt

if __name__ == '__main__':
    if False:
        hh, mm, ss = 00, 23, 00
        name, y, d = 'Filipe', 33, 5000

    if True:
        name = raw_input('Name: ')
        y = int(raw_input('Age: '))
        d = float(raw_input('Distance in meters: '))
        time = raw_input('Time HH MM SS: ')
        hh, mm, ss = [int(n) for n in time.split()]

    t = float(hh) * 60. + float(mm) + float(ss) / 60
    v = vo2(t, d)
    p = pvmax(t)
    vm = vo2max(v, p)
    hrmax = 206.3 - (0.711 * y)
    phrmax = 0.63 * p + 0.37
    hr = phrmax * hrmax

    t1 = np.fliplr(60 * _estt(x, pvm * vm))
    r1 = np.fliplr(1000 * t1 / x[..., None])

    cols0 = ('%i%%,%i%%,%i%%,%i%%,%i%%,%i%%,%i%%,%i%%,%i%%,%i%%' %
             tuple(Nint(pvm * 100))[::-1])
    cols1 = ('%i%%,%i%%,%i%%,%i%%,%i%%,%i%%,%i%%,%i%%,%i%%,%i%%' %
             tuple(Nint(phr * 100))[::-1])

    t1 = DataFrame(t1, index=x, columns=cols0.split(',')).applymap(d2hms)
    r1 = DataFrame(r1, index=x, columns=cols1.split(',')).applymap(d2hms)

    # Text output.
    lines0 = [
        u'Atleta:,%s' % name,
        u'Idade:,%i,anos' % y,
        u'Distância,base:,%s,m' % d,
        u'Tempo,base:,%02i:%02i:%02i' % (hh, mm, ss),
        u'',
        u'VO2,estimado:,%i,ml/kg/min' % np.round(v),
        (u'Equivalente,a,%i%%,do,VO2,máximo:%i,ml/kg/min' %
         (Nint(p * 100), Nint(vm))),
        u'',
        u'Ritmo,cardíaco:,%i,bpm' % Nint(hr),
        (u'Equivalente,a,%i%%,do,ritmo,cardíaco,máximo:,%i,bpm' %
         (Nint(phrmax * 100), Nint(hrmax))),
        u'',
        u'Tempos,Estimados,e,%VO2,Max',
        u'']
    lines1 = to_csv(t1)
    lines2 = [u'', u'Ritmos,Estimados,e,%Max,Ritmo,Cardíaco']
    lines3 = to_csv(r1)

    write_spreadsheet('corrida.csv', lines0 + lines1 + lines2 + lines3)
