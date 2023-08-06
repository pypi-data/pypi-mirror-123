# !/usr/bin/env python
# coding: utf-8
# version: 1.0
# author: Fennel
# contact: gongkangjia@gmail.com
# date: 2021/5/13
import re
import ast


_coord = ['COORDTYPE', 'P_ALP', 'P_BET', 'P_GAM', 'XCENT', 'YCENT']
_grid = [
    'COORDNAME',
    'XORIG',
    'YORIG',
    'XCELL',
    'YCELL',
    'NCOLS',
    'NROWS',
    'NTHIK']

# 投影类型
_gdnames = {1: "latitude_longitude",
            2: "lambert_conformal_conic",
            7: "mercator",
            6: "polar_stereographic"}


class Coord:
    def __init__(self, name, **kwargs):
        self.name = name
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return "<Coord.{}>".format(self.__dict__)

    def __repr__(self):
        return "<Coord.{}>".format(self.__dict__)


class Grid:
    """
    <Grid.{'name': 'YRD12_LYG',
     'coord': <Coord.{'name': 'LAM_32N', 'COORDTYPE': 2,
      'P_ALP': 30.0, 'P_BET': 60.0,
       'P_GAM': 118.0, 'XCENT': 118.0, 'YCENT': 32.0}>,
     'COORDNAME': 'LAM_32N',
     'XORIG': -582000.0,
     'YORIG': -402000.0,
     'XCELL': 12000.0,
     'YCELL': 12000.0,
     'NCOLS': 110,
     'NROWS': 90,
     'NTHIK': 1}>

    """

    def __init__(self, name, coord, **kwargs):
        self.name = name
        self.coord = coord
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return "<Grid.{}>".format(self.__dict__)

    def __repr__(self):
        return "<Grid.{}>".format(self.__dict__)

    def get_map(self, **kwargs):
        from mpl_toolkits.basemap import Basemap
    #     from .conventions.ioapi import get_ioapi_sphere
        if (
                getattr(self.coord, "COORDTYPE", 0) in (2, 6, 7) and
                all([hasattr(self.coord, k) for k in ("P_GAM", "P_ALP", "P_BET")]) and
                all([hasattr(self, k)
                     for k in ("XORIG", "YORIG", "XCELL", "YCELL")])
        ):

            llcrnrx = self.XORIG
            urcrnrx = self.XORIG + self.NCOLS * self.XCELL

            llcrnry = self.YORIG
            urcrnry = self.YORIG + self.NROWS * self.YCELL

            # semi_major_axis, semi_minor_axis = get_ioapi_sphere()
            semi_major_axis, semi_minor_axis = (6370997, 6370997)
            if self.coord.COORDTYPE == 2:
                from mpl_toolkits.basemap import pyproj
                p = pyproj.Proj(proj='lcc', a=semi_major_axis, b=semi_major_axis,
                                lon_0=self.coord.P_GAM, lat_1=self.coord.P_ALP,
                                lat_2=self.coord.P_BET, lat_0=self.coord.YCENT)
                llcrnrlon, llcrnrlat = p(llcrnrx, llcrnry, inverse=True)
                urcrnrlon, urcrnrlat = p(urcrnrx, urcrnry, inverse=True)
                m = Basemap(projection='lcc',
                            rsphere=(semi_major_axis, semi_major_axis),
                            lon_0=self.coord.P_GAM, lat_1=self.coord.P_ALP,
                            lat_2=self.coord.P_BET, lat_0=self.coord.YCENT,
                            llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat,
                            urcrnrlat=urcrnrlat, urcrnrlon=urcrnrlon,
                            **kwargs)
                return m
            else:
                raise("Only lcc")
        else:
            raise ("Only lcc")


class GRIDDESC:
    def __init__(self, filepath):
        self.filepath = filepath
        self._coords = {}
        self._grids = {}
        self._parse()

    def get_coord(self, coord_name):
        return self._coords[coord_name]

    def get_grid(self, grid_name):
        return self._grids[grid_name]

    @property
    def coords(self):
        return self._coords.keys()

    @property
    def grids(self):
        return self._grids.keys()

    def _parse(self):

        with open(self.filepath) as f:
            griddesc = f.read()

        griddesc = re.sub(r'!.*?(?=(\n|$))', '', griddesc)

        griddesc_lines = [i.strip() for i in griddesc.strip().split('\n') if i]

        assert griddesc_lines[-1] == "' '"

        blank_counter = 0

        i = 0
        while i < len(griddesc_lines):
            line = griddesc_lines[i]

            if line == "' '":
                blank_counter += 1
            else:
                i += 1
                cells = []
                for c in griddesc_lines[i].split():
                    c = c.strip("', ")
                    try:
                        # print(c)
                        cells.append(ast.literal_eval(c))
                    except Exception as e:
                        cells.append(c)

                key = eval(line)

                if blank_counter == 1:
                    self._coords[key] = Coord(
                        name=key, **dict(zip(_coord, cells)))
                elif blank_counter == 2:
                    # print(cells)
                    grid_dict = dict(zip(_grid, cells))
                    # print(grid_dict)
                    self._grids[key] = Grid(
                        name=key, coord=self.get_coord(
                            grid_dict["COORDNAME"]), **grid_dict)
            i += 1


if __name__ == '__main__':
    griddesc = GRIDDESC("../examples/GRIDDESC3")
    # print(griddesc.coords)
    # print(griddesc.grids)
    # print("*" * 10)
    grid = griddesc.get_grid("YJG")
    # print(grid)
    # print(grid.coord.name)
    # print(grid.get_map())
