#!/usr/bin/env python
# -*- coding: utf-8 -*-
#mirlight by grizz - Witek Firlej http://grizz.pl
# Copyright (C) 2009-2010 Witold Firlej
#
# To build an .exe file use: python setup_win_exe.py py2exe --includes sip

from distutils.core import setup
import py2exe

# zipfile=None ## To create one large exe - uncoment this, and use --bundle 1 option

setup(windows=[{"script" : "mirlight_gui.py"}],options={"py2exe":{"includes":["sip"]}})
