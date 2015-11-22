#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

## Зададим переменную окружения GISBASE
gisbase = os.environ['GISBASE'] = "/usr/lib/grass70"
## Зададим переменную окружения GISBASE
gisdbase = os.path.join(os.environ['HOME'], "grassdata")
## Зададим переменные LOCATION и MAPSET
location = "gisconf"
mapset   = "PERMANENT"
sys.path.append(os.path.join(os.environ['GISBASE'], "etc", "python"))
# Импортируем Python-модуль GRASS 
import grass.script as grass
import grass.script.setup as gsetup
# Запускаем сессию GRASS
gsetup.init(gisbase, gisdbase, location, mapset)
print grass.gisenv()
