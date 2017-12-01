
#! /usr/env/bin python
# -*- coding: utf-8 -*-
import os
import re
import logging
dir_path = os.listdir(os.path.abspath(os.path.dirname(__file__)))

# xxx_handler xx leng must > 1.
hander_files = [x for x in dir_path if re.findall('[A-Za-z]\w+_handler\.py$', x)]

for hander_file in hander_files:
    model_name = hander_file[:-3]
    logging.warn("handler [%s] register success!" % hander_file)
    __import__(model_name, globals(), locals(), [model_name], -1)
