#!/usr/bin/env python
# -*- coding: utf-8 -*-

#%Module
#% description: Module example
#% overwrite: yes
#%End
#%option
#% key: input
#% type: string
#% required: yes
#% multiple: no
#% key_desc: name
#% label: Input map
#% gisprompt: old,vector,vector
#%end
#%option
#% key: zcolumn
#% type: string
#% required: yes
#% multiple: no
#% key_desc: name
#% label: Field with heights
#% gisprompt: old,dbcolumn,dbcolumn
#% guisection: Parameters
#%end
#%option
#% key: output
#% type: string
#% required: yes
#% multiple: no
#% key_desc: name
#% description: Output map
#% gisprompt: new,cell,raster
#% guisection: Outputs
#%end
#%option
#% key: test_map
#% type: string
#% required: yes
#% multiple: no
#% key_desc: name
#% label: Test input map
#% gisprompt: old,vector,vector
#% guisection: Parameters
#%end
#%option
#% key: smooth_step
#% type: double
#% required: yes
#% multiple: no
#% description: Smooth step
#% guisection: Parameters
#%end
#%option
#% key: tension_step
#% type: double
#% required: yes
#% multiple: no
#% description: Tension step
#% guisection: Parameters
#%end
#%option
#% key: smooth_max
#% type: double
#% required: yes
#% multiple: no
#% description: Smooth max value
#% guisection: Parameters
#% answer: 10
#%end
#%option
#% key: tension_max
#% type: double
#% required: yes
#% multiple: no
#% description: Tension max value
#% guisection: Parameters
#% answer: 100
#%end


import uuid

import grass.script as grass

def get_error(input_map, zcol, test_map, smooth, tension):
    output_map = uuid.uuid4().hex
    grass.run_command('g.region', vect=input_map)
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
            tension_step, smooth_max=10, tension_max=100):
    opt = 10000000  #
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


def main(input_map, zcol, test_map, smooth_step, tension_step,
         smooth_max, tension_max):
    smooth, tension = optimize(input_map, 'value',
                               test_map, smooth_step, tension_step,
                               smooth_max, tension_max)
    print smooth, tension
    grass.run_command('v.surf.rst', input=input_map, elev=output_map,
        zcol=zcol, smooth=smooth, tension=tension,
        segmax=30, npmin=140, overwrite=True)


if __name__ == "__main__":
    options, flags = grass.parser()

    input_map = options['input']
    output_map = options['output']
    zcol = options['zcolumn']
    test_map = options['test_map']
    smooth_step = float(options['smooth_step'])
    tension_step = float(options['tension_step'])
    smooth_max = int(options['smooth_max'])
    tension_max = int(options['tension_max'])


    main(input_map, zcol, test_map, smooth_step, tension_step,
         smooth_max, tension_max)


