#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
# grass7bin = r'C:\OSGeo4W\bin\grass70.bat'
# Зададим переменную GISBASE
gisbase = os.environ['GISBASE'] = r'C:\OSGeo4W\apps\grass\grass-7.0.2'
# os.environ['PATH'] += os.pathsep + os.path.join(gisbase, 'extrabin')
# # Set GISDBASE environment variable
# gisdb = os.environ['GISDBASE'] = os.path.join('E:', 'gisconf_grass')
# location = 'E:\gisconf_grass'
# mapset = 'user1'
# # define GRASS-Python environment
# gpydir = os.path.join(gisbase, 'etc', 'python')
# sys.path.append(gpydir)
# # import GRASS Python bindings
# import grass.script as gscript
# import grass.script.setup as gsetup
# # launch session
# gsetup.init(gisbase, gisdb, location, mapset)
# print grass.gisenv()
