#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

def main(mapset, altitude):
    grass.run_command('g.mapset', mapset=mapset, flags='c')

    grass.run_command('g.region', raster='elev_2m')
    grass.run_command('g.list', type='raster')


    names = []
    for a in range(0, 360, 20):
        shaded = 'elev_sh_' + str(a)
        grass.run_command('r.relief', input='elev_2m', altitude=altitude,
                          output=shaded, azimuth=a, overwrite=True)
        shaded_color = 'elev_sh_col_' + str(a)
        grass.run_command('r.shade', shade=shaded, color='elevation',
                          output=shaded_color, overwrite=True)

        names.append(shaded_color)

if __name__ == "__main__":
    gisbase = sys.argv[1]
    grassdata = sys.argv[2]
    location = sys.argv[3]
    mapset = sys.argv[4]
    altitude = sys.argv[5]

    os.environ['GISBASE'] = gisbase
    sys.path.append(os.path.join(os.environ['GISBASE'], "etc", "python"))
    path = os.getenv('LD_LIBRARY_PATH')
    if path is None:
        os.environ['LD_LIBRARY_PATH'] = os.path.join(gisbase, 'lib')

    import grass.script as grass
    import grass.script.setup as gsetup

    gsetup.init(gisbase, grassdata, location, 'PERMANENT')
    main(mapset, altitude)


