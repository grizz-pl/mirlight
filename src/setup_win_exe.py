#!/usr/bin/env python
# -*- coding: utf-8 -*-
#mirlight by grizz - Witek Firlej http://grizz.pl
# Copyright (C) 2009-2010 Witold Firlej
#
# To build an .exe file use: python setup_win_exe.py py2exe

from distutils.core import setup
import py2exe

setup(windows=[{"script" : "mirlight_gui.py", "icon_resources": [(0, "mirlight.ico")]}],zipfile=None,options={"py2exe":{"includes":["sip"],"bundle_files": 1}})
