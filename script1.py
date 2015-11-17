#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grass.script as grass

import uuid

def get_error(input_map, zcol, test_map, smooth, tension):
    output_map = uuid.uuid4().hex
    grass.run_command('v.surf.rst', input=input_map, elev=output_map,
        zcol=zcol, smooth=smooth, tension=tension,
        segmax=30, npmin=140, overwrite=True)
    grass.run_command('v.what.rast', map=test_map, raster=output_map, column='elev')
    grass.run_command('v.db.update', map=test_map, column='error',
    query_column="value - elev")
    # Удалим временную карту высот
    grass.run_command('g.remove', type='raster', name=output_map, flags='f')

    result = grass.parse_command('v.univar', map=test_map,
                                 column='error', flags='g')
    return result

def optimize(input_map, zcol, test_map, smooth_step,
            tension_step, smooth_max=100, tension_max=200):
    opt = 10000000  # Большое число
    tens = sm = None
    s = t = 0
    while s< smooth_max:
        while t < tension_max:
            err = get_error(input_map, zcol, test_map, s, t)
            err = float(err['mean_abs'])
            if err < opt:
                opt = err
                tens = t
                sm = s
            t = t + tension_step
        s = s + smooth_step
    return sm, tens


if __name__ == "__main__":
    input_map = 'elev_points'
    output_map = 'elev_2m'
    zcol = 'value'
    test_map = 'test'

    smooth, tension = optimize(input_map, zcol,
                               test_map, smooth_step=20, tension_step=30)
    print smooth, tension
    grass.run_command('v.surf.rst', input=input_map, elev=output_map,
        zcol=zcol, smooth=smooth, tension=tension,
        segmax=30, npmin=140, overwrite=True)
