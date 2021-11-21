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

    #-- Writing to File
    with open(jparams['output-file'], 'w') as f:
        f.write(f"NCOLS {ncols}\n"
                f"NROWS {nrows}\n"
                f"XLLCORNER {min_x}\n"
                f"YLLCORNER {min_y}\n"
                f"CELLSIZE {jparams['cellsize']}\n"
                f"NODATA_VALUE -9999\n")
        for row in range(nrows, 0, -1):  # from the left-upper corner
            for column in range(ncols):
                rgrid = [min_x + column * jparams['cellsize'] + 0.5 * jparams['cellsize'],
                         min_y + row * jparams['cellsize'] - 0.5 * jparams['cellsize']]
                dd, ii = nnTree.query(rgrid)
                z_val = list_pts_3d[ii]
                f.write(str(z_val[2]))
                f.write(' ')

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
    nodata_value = -9999

    print("cellsize:", jparams['cellsize'])
    print("radius:", jparams['radius1'])
    print("power:", jparams['power'])
    print("radius1:", jparams['radius1'])
    print("radius2:", jparams['radius2'])
    print("angle:", jparams['angle'])
    print("max_points:", jparams['max_points'])
    print("min_points:", jparams['min_points'])

    # #-- CONVEX HULL
    # hull = scipy.spatial.ConvexHull(2d_xy)

    #-- to speed up the nearest neighbour us a kd-tree
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html#scipy.spatial.KDTree
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.query.html#scipy.spatial.KDTree.query
    # kd = scipy.spatial.KDTree(list_pts)
    # i = kd.query_ball_point(p, radius)

    idwTree = scipy.spatial.KDTree(list_pts_3d)

    min_x, min_y = idwTree.mins[0], idwTree.mins[1]
    max_x, max_y = idwTree.maxes[0], idwTree.maxes[1]

    # -- BOUNDING BOX (BBOX)
    bound_x = max_x - min_x
    bound_y = max_y - min_y

    # -- Calculate NCOLS and NROWS
    ncols = int(math.ceil(bound_x / jparams['cellsize']))
    nrows = int(math.ceil(bound_y / jparams['cellsize']))

    idwList = idwTree.query_ball_point(list_pts_3d, jparams['radius1'])

    #-- Writing to file
    with open(jparams['output-file'], 'w') as idwFile:
        idwFile.write(f"NCOLS {ncols}\n")
        idwFile.write(f"NROWS {nrows}\n")
        idwFile.write(f"XLLCORNER {min_x}\n")
        idwFile.write(f"YLLCORNER {min_y}\n")
        idwFile.write(f"CELLSIZE {jparams['cellsize']} \n")
        idwFile.write(f"NODATA_VALUE {nodata_value}\n")
        idwFile.write(f"{idwTree.size}")

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
    #
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
