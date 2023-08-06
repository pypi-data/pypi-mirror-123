# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 22:50:32 2021

@author: mumuz
"""

import os
import clr

LIB_PATH = os.path.abspath(os.path.dirname(__file__))

# 加载Mumu.SWMM.SwmmObjects.dll
clr.AddReference(LIB_PATH + '\\Mumu.SWMM.SwmmObjects.dll')
# 加载Mumu.SWMM.Output.dll
clr.AddReference(LIB_PATH + '\\Mumu.SWMM.Output.dll')