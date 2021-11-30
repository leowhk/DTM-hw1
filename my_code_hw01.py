#-- my_code_hw01.py
#-- hw01 GEO1015.2021
#-- [YOUR NAME]
#-- [YOUR STUDENT NUMBER] 
#-- [YOUR NAME]
#-- [YOUR STUDENT NUMBER] 


#-- import outside the standard Python library are not allowed, just those:
import math
import numpy
import scipy.spatial
import startinpy

import random
#-----

def grid_write(list_pts_3d, jparams):
    cellsize = jparams['cellsize']
    x = []
    y = []
    list_pts= []
    r_grid = []

    # -- CONVERT TO 2D XY
    for p in list_pts_3d:
        x.append(p[0])
        y.append(p[1])
        list_pts.append([p[0], p[1]])

    min_x, min_y= min(x), min(y)
    max_x, max_y = max(x), max(y)

    # -- BOUNDING BOX (BBOX)
    bound_x = max_x - min_x
    bound_y = max_y - min_y

    # -- CELL SIZE
    ncols = math.ceil(bound_x / cellsize)
    nrows = math.ceil(bound_y / cellsize)

    # -- GRID POINTS
    for row in range(nrows, 0, -1):  # FROM LEFT UPPER CORNER
        for column in range(ncols):
            x_coord = min_x + column * jparams['cellsize'] + 0.5 * jparams['cellsize']
            y_coord = min_y + row * jparams['cellsize'] - 0.5 * jparams['cellsize']
            grid_coord = [x_coord, y_coord]
            r_grid.append(grid_coord)

    asc = "NCOLS {}\nNROWS {}\nXLLCORNER {}\nYLLCORNER {}\nCELLSIZE {}\nNODATA_VALUE -9999\n".format(ncols, nrows, min_x, min_y, cellsize)


    return list_pts, asc, nrows, ncols, min_x, min_y, r_grid

# def is_point_inside_ellipse(pt, polygon, on=True):
#     """
#     Function that tests if a point is inside a polygon.
#
#     Input:
#         pt:         the point to test (a tuple of coordinates)
#         polygon:    a ring of the polygon represented by a list of tuple.
#         on:         if the point on the boundary is considered inside. 'True' means inside and vice versa.
#     Output:
#         True:       pt is inside polygon
#         False:      pt is outside polygon
#     """
#     flag = False
#     for i in range(len(polygon) - 1):
#         x = pt[0]
#         y = pt[1]
#         x1 = polygon[i][0]
#         y1 = polygon[i][1]
#         x2 = polygon[i + 1][0]
#         y2 = polygon[i + 1][1]
#
#         if on and ((x == x1 and y == y1) or (
#                 x == x2 and y == y2)):  # pt is on the border (one of the vertices) of the polygon
#             return True
#
#         if y1 <= y < y2 or y2 <= y < y1:
#             x_crossing_point = (x2 - x1) / (y2 - y1) * (y - y1) + x1
#             if on and x_crossing_point == x:  # pt is on the border (not horizontal lines) of the polygon
#                 return True
#             elif x_crossing_point > x:  # pt is inside (not on the border of) the polygon
#                 flag = not flag
#         elif on and y1 == y == y2:
#             if x1 < x < x2 or x2 < x < x1:  # pt is on the border (horizontal lines) of the polygon
#                 return True
#     return flag

def nn_interpolation(list_pts_3d, jparams):
    """
    !!! TO BE COMPLETED !!!
     
    Function that writes the output raster with nearest neighbour interpolation
     
    Input:
        list_pts_3d: the list of the input points (in 3D) (list of lists)
        jparams:     the parameters of the input for "nn"
    Output:
        (output file written to disk)
 
    """
    print("cellsize:", jparams['cellsize'])

    #-- to speed up the nearest neighbour use a kd-tree
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html#scipy.spatial.KDTree
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.query.html#scipy.spatial.KDTree.query
    # kd = scipy.spatial.KDTree(list_pts_3d)
    # d, i = kd.query(p, k=1)

    cellsize = jparams['cellsize']
    x = []
    y = []
    list_pts_xy = []

    #-- CONVERT TO 2D XY
    for p in list_pts_3d:
        x.append(p[0])
        y.append(p[1])
        list_pts_xy.append([p[0], p[1]])

    nnTree = scipy.spatial.KDTree(list_pts_xy)

    min_x, min_y = nnTree.mins[0], nnTree.mins[1]
    max_x, max_y = nnTree.maxes[0], nnTree.maxes[1]

    #-- BOUNDING BOX (BBOX)
    bound_x = max_x - min_x
    bound_y = max_y - min_y

    #-- CELL SIZE = 2.0
    ncols = int(math.ceil(bound_x / jparams['cellsize']))
    nrows = int(math.ceil(bound_y / jparams['cellsize']))

    # #-- RASTER GRID POINTS
    # raster = []
    # all_i = []
    # for row in range(nrows, 0, -1):  # from the left-upper corner
    #     for column in range(ncols):
    #         rgrid = [min_x + column * jparams['cellsize'] + 0.5 * jparams['cellsize'], min_y + row * jparams['cellsize'] - 0.5 * jparams['cellsize']]
    #         dd, ii = nnTree.query(rgrid)
    #         raster.append(rgrid)
    #         all_i.append(ii)

    raster = []
    all_i = []

    #-- WRITING TO FILE
    with open(jparams['output-file'], 'w') as f:
        f.write(f"NCOLS {ncols}\n"
                f"NROWS {nrows}\n"
                f"XLLCORNER {min_x}\n"
                f"YLLCORNER {min_y}\n"
                f"CELLSIZE {jparams['cellsize']}\n"
                f"NODATA_VALUE -9999\n")
        for row in range(nrows, 0, -1):  # FROM LEFT UPPER CORNER
            for column in range(ncols):
                rgrid = [min_x + column * jparams['cellsize'] + 0.5 * jparams['cellsize'],
                         min_y + row * jparams['cellsize'] - 0.5 * jparams['cellsize']]
                dd, ii = nnTree.query(rgrid)
                z_val = list_pts_3d[ii]
                f.write(str(z_val[2]))
                f.write('\n')

    print("File written to", jparams['output-file'])

def idw_interpolation(list_pts_3d, jparams):
    """
    !!! TO BE COMPLETED !!!
     
    Function that writes the output raster with IDW
     
    Input:
        list_pts_3d: the list of the input points (in 3D)
        jparams:     the parameters of the input for "idw"
    Output:
        (output file written to disk)
 
    """
    print("cellsize:", jparams['cellsize'])
    print("radius:", jparams['radius1'])
    print("power:", jparams['power'])
    print("radius1:", jparams['radius1'])
    print("radius2:", jparams['radius2'])
    print("angle:", jparams['angle'])
    print("max_points:", jparams['max_points'])
    print("min_points:", jparams['min_points'])

    power = jparams['power']
    r1 = jparams['radius1']
    r2 = jparams['radius2']
    a = math.radians(jparams['angle'])

    # #-- CONVEX HULL
    # hull = scipy.spatial.ConvexHull(2d_xy)

    #-- to speed up the nearest neighbour us a kd-tree
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html#scipy.spatial.KDTree
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.query.html#scipy.spatial.KDTree.query
    # kd = scipy.spatial.KDTree(list_pts)
    # i = kd.query_ball_point(p, radius)

    x, y, list_pts_xy = [], [], []

    #-- CONVERT TO 2D XY
    for p in list_pts_3d:
        x.append(p[0])
        y.append(p[1])
        list_pts_xy.append([p[0], p[1]])
        sample_coord = tuple(p[0], p[1])


    idwTree = scipy.spatial.KDTree(list_pts_xy)

    min_x, min_y = idwTree.mins[0], idwTree.mins[1]
    max_x, max_y = idwTree.maxes[0], idwTree.maxes[1]

    #-- BOUNDING BOX (BBOX)
    bound_x = max_x - min_x
    bound_y = max_y - min_y

    #-- CELL SIZE = 2.0
    ncols = int(math.ceil(bound_x / jparams['cellsize']))
    nrows = int(math.ceil(bound_y / jparams['cellsize']))

    # ellipse = (((j[0] - i[0]) * math.cos(a) + (j[1] - i[1]) * math.sin(a)) ** 2 / r1 ** 2) + (((j[0] - i[0]) * math.sin(a) + (j[1] - i[1]) * math.cos(a)) ** 2 / r2 ** 2)

    rgrid = []
    #-- Writing to file
    with open(jparams['output-file'], 'w') as f:
        f.write(f"NCOLS {ncols}\n"
                f"NROWS {nrows}\n"
                f"XLLCORNER {min_x}\n"
                f"YLLCORNER {min_y}\n"
                f"CELLSIZE {jparams['cellsize']}\n"
                f"NODATA_VALUE -9999\n")
        for row in range(nrows, 0, -1):  # from the left-upper corner
            for column in range(ncols):
                x_coord = min_x + column * jparams['cellsize'] + 0.5 * jparams['cellsize']
                y_coord = min_y + row * jparams['cellsize'] - 0.5 * jparams['cellsize']
                raster_coord = (x_coord, y_coord)


                dist_less_than_fifteen = []
                for i in range(len(list_pts_xy)):
                    dist = math.hypot(x[i], y[i], x_coord, y_coord)
                    if dist <= 15:
                        dist_less_than_fifteen.append(dist)
                        f.write(f"({i}, {dist_less_than_fifteen}) ")
        f.write("\n end")


                    # search_ellipse = (((x[i] - x_coord) * math.cos(a) + (y[i] - y_coord) * math.sin(a)) ** 2 / r1 ** 2) + (((x[i] - x_coord) * math.sin(a) + (y[i] - y_coord) * math.cos(a)) ** 2 / r2 ** 2)

                # if search_ellipse <= 1:
                #     pt_results.append([xxx, yyy])


                # for i in range(0, len(list_pts_xy), 1):
                #     dist = math.hypot(x[i], y[i], x_coord, y_coord)

                # ellipse = (((x[i] - x_coord) * math.cos(a) + (y[i] - y_coord) * math.sin(a)) ** 2 / r1 ** 2) + \
                #           (((x[i] - x_coord) * math.sin(a) + (y[i] - y_coord) * math.cos(a)) ** 2 / r2 ** 2)

                # rgrid = [min_x + column * jparams['cellsize'] + 0.5 * jparams['cellsize'],
                #          min_y + row * jparams['cellsize'] - 0.5 * jparams['cellsize']]
                # dd, ii = idwTree.query(rgrid)
                # z_val = list_pts_3d[ii]
                # f.write(str(z_val[2]))

    print("File written to", jparams['output-file'])


def tin_interpolation(list_pts_3d, jparams):
    """
    !!! TO BE COMPLETED !!!
     
    Function that writes the output raster with linear in TIN interpolation
     
    Input:
        list_pts_3d: the list of the input points (in 3D)
        jparams:     the parameters of the input for "tin"
    Output:
        (output file written to disk)
 
    """  
    #-- example to construct the DT with scipy
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Delaunay.html#scipy.spatial.Delaunay
    # dt = scipy.spatial.Delaunay([])

    #-- example to construct the DT with startinpy
    # minimal docs: https://github.com/hugoledoux/startinpy/blob/master/docs/doc.md
    # how to use it: https://github.com/hugoledoux/startinpy#examples
    # you are *not* allowed to use the function for the tin linear interpolation that I wrote for startinpy
    # you need to write your own code for this step
    # but you can of course read the code [dt.interpolate_tin_linear(x, y)]


    #-- writing to file ar
    # with open(jparams['output-file'], 'w') as f:
    #     f.write('ok it is written la')

    print("File written to", jparams['output-file'])


def laplace_interpolation(list_pts_3d, jparams):
    """
    !!! TO BE COMPLETED !!!
     
    Function that writes the output raster with Laplace interpolation
     
    Input:
        list_pts_3d: the list of the input points (in 3D)
        jparams:     the parameters of the input for "laplace"
    Output:
        (output file written to disk)
 
    """  
    #-- example to construct the DT with scipy
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Delaunay.html#scipy.spatial.Delaunay
    # dt = scipy.spatial.Delaunay([])

    #-- example to construct the DT with startinpy
    # minimal docs: https://github.com/hugoledoux/startinpy/blob/master/docs/doc.md
    # how to use it: https://github.com/hugoledoux/startinpy#examples
    # you are *not* allowed to use the function for the laplace interpolation that I wrote for startinpy
    # you need to write your own code for this step


    #-- writing to file ar
    # with open(jparams['output-file'], 'w') as f:
    #     f.write('ok it is written la')
    #
    print("File written to", jparams['output-file'])
