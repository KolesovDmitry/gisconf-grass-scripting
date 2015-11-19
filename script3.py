#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import shutil

def main(grassdata, location, mapset, altitude):
    # Создаем временный Mapset
    grass.run_command('g.mapset', mapset=mapset, flags='c')

    # Копируем туда файлыё
    grass.run_command('g.copy', raster='elev_2m@user1,elev_2m')
    grass.run_command('g.region', raster='elev_2m')

    # Отмывка рельефа
    names = []
    for a in range(0, 360, 20):
        shaded = 'elev_sh_' + str(a)
        grass.run_command('r.relief', input='elev_2m', altitude=altitude,
                          output=shaded, azimuth=a, overwrite=True)
        shaded_color = 'elev_sh_col_' + str(a)
        grass.run_command('r.shade', shade=shaded, color='elevation',
                          output=shaded_color, overwrite=True)
        names.append(shaded_color)

    # Переходим в PERMANENT, копируем результаты расчетов
    grass.run_command('g.mapset', mapset='PERMANENT', flags='c')
    for name in names:
        name_old = name + '@' + mapset
        grass.run_command('g.copy', raster=name_old +',' + name)

    # Удаляем временный MAPSET
    shutil.rmtree(os.path.join(grassdata, location, mapset))

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
    main(grassdata, location, mapset, altitude)


