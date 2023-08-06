# !/usr/bin/env python
# coding: utf-8
# version: 1.0
# author: Fennel
# contact: gongkangjia@gmail.com
# date: 2021/5/28
import os
import pyioapi
import xarray as xr
import pathlib
data = xr.open_dataset(pathlib.Path(__file__).parent.resolve()/"METCRO3D_2019-05-01",engine="ioapi")
print(data)
