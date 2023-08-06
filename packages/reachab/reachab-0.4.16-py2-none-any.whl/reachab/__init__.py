# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Reachability Analysis
#
# (C) 2020 Michael Hartmann, Graz, Austria
# Released under GNU GENERAL PUBLIC LICENSE
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------
import reachab.src.reachability as rb
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from shapely.geometry import Polygon, Point
import numpy as np
from reachab.src.states_reachsets import *
import copy


def points_inside_hull(zonoset):
    all_inside_points=get_sample_points_inside_hull(zonoset)
    return all_inside_points


def plot_all_inside_points(all_inside_points):
    colors=["red", "orange", "yellow", "cyan", "blue", "black", "red", "orange", "yellow", "cyan", "blue", "black"]
    for idx, act_points in enumerate(all_inside_points):
        for act_point in act_points:
            plt.arrow(act_point[0], act_point[1], 0.1*act_point[2], 0.1*act_point[3],
                      fc=colors[idx], ec="black", alpha=1, width=.3,
                      head_width=.7, head_length=.83)



'''
    Test me function. A user should see if the program is installed and a simple plot is available 
'''
def test_me():
    obj_reachability = rb.reachability()
    obj_reachability.test_function()



'''
    Reachability Analysis. 
    Omega_0: Initial state set
    U: Fixed control input set
    Params: Parameters
'''
def reach(Omega_0, U, params):
    ##################################
    ## REACHABILITY ANALYSIS PARAMS ##
    ##################################
    ra_params = {
        'T': params['time_horizon'],
        'N': params['steps'],
    }
    erg=[]
    obj_reach = rb.reachability(**ra_params)
    program = ['without_box', 'with_box']
    if (program[0] == params['box_function']):
        R, X = obj_reach.approximate_reachable_set_without_box(Omega_0, U)
    elif (program[1] == params['box_function']):
        R, X = obj_reach.approximate_reachable_set_with_box(Omega_0, U)
    for act_zono in R:
        zonoset, unique_vec = obj_reach.get_points_of_zonotype(act_zono)
        if (params['visualization'] == 'y'):
            obj_reach.obj_visual.filled_polygon(zonoset, params['face_color'], .2)
        erg.append(zonoset)
    #points_a=states_for_R(params, obj_reach, R)
    return erg


def transform_homogenous_sets(obj_reach, X):
    R=X
    for idx, q_zono in enumerate(R):
        act_idx=idx-1
        q_zono['c']=q_zono['c']+np.matrix([[-act_idx*act_idx*.4], [act_idx*act_idx*.8],[0], [0]])
        q_zono['g']=q_zono['g']+np.matrix([[act_idx*act_idx*.04, 0], [0, act_idx*act_idx*.13],[0, 0], [0, 0]])

        zonoset, unique_vec = obj_reach.get_points_of_zonotype(q_zono)
        obj_reach.obj_visual.filled_polygon(zonoset, 'red', 1)


def reach_zonotype_without_box(Omega_0, U, **kwargs):
    ##################################
    ## REACHABILITY ANALYSIS PARAMS ##
    ##################################
    homogenous_zonoset = []
    erg_zonoset=[]
    ra_params = {
        'T': kwargs["time_horizon"],
        'N': kwargs["steps"],
    }
    obj_reach = rb.reachability(**ra_params)
    copy_obj_reach=copy.deepcopy(obj_reach)
    R, X = obj_reach.approximate_reachable_set_without_box(Omega_0, U)
    copy_R, copy_X = copy_obj_reach.approximate_reachable_set_without_box(Omega_0, U)
    if (kwargs['transformed_visualization'] == 'y'):
        transform_homogenous_sets(copy_obj_reach, copy_X)
    for idx, act_zono in enumerate(X):
        zonoset, unique_vec = obj_reach.get_points_of_zonotype(act_zono)
        if (kwargs['homogenous_visualization'] == 'y'):
            obj_reach.obj_visual.filled_polygon(zonoset, 'orange', .6)
        homogenous_zonoset.append(unique_vec)

    for act_zono in R:
        zonoset, unique_vec = obj_reach.get_points_of_zonotype(act_zono)
        if (kwargs['visualization'] == 'y'):
            obj_reach.obj_visual.filled_polygon(zonoset, kwargs['face_color'], .2)
        erg_zonoset.append(unique_vec)
    return R, X, obj_reach, erg_zonoset

def get_zonotype_points(obj_reach, R):
    erg = []
    for act_zono in R:
        zonoset = obj_reach.get_points_of_zonotype(act_zono)
        erg.append(zonoset)
    return erg

'''
    Show the plots
'''
def show_all():
    plt.axis('equal')
    plt.grid("on")
    plt.xlabel("x [m]", fontsize=12)
    plt.ylabel("y [m]", fontsize=12)
    plt.show()


'''
    Get states for reach sets R
'''
def states_for_R(params, obj_reach, R):
    act_zono=R[-1]
    points=obj_reach.get_points_of_zonotype(act_zono)
    tuple_points=[(points[0][i], points[1][i]) for i in range(0, len(points[0]))]
    poly = Polygon(tuple_points)
    minx, miny, maxx, maxy = poly.bounds
    x=np.linspace(minx, maxx, params['nx'])
    y=np.linspace(miny, maxy, params['ny'])
    xv, yv = np.meshgrid(x, y)
    x_vec=np.ravel(xv)
    y_vec = np.ravel(yv)

    list_points=[]
    for i in range(0, len(x_vec)):
        a_x=x_vec[i]
        a_y=y_vec[i]
        # print(a_x, a_y)
        new_point=Point(a_x, a_y)
        bool_test=is_point_in_polygon(new_point, poly)
        if(bool_test == True):
            list_points.append((a_x, a_y))
    return list_points


'''
    Is point in polygon
'''
def is_point_in_polygon(point, poly):
    if poly.contains(point):
        return True
    else:
        return False

'''
    Get states for reach sets R
'''
def get_points_zonotype(zonotype):
    obj_reachability = rb.reachability()
    return obj_reachability.get_points_of_zonotype(zonotype)

'''
    Compute velocity with Savgol Golay Filter
'''
def compute_velocity(trajectory, window_size=70, polyorder=2):
    rx = trajectory[0]
    ry = trajectory[1]
    vx = savgol_filter(rx, window_size, polyorder, 1)
    vy = savgol_filter(ry, window_size, polyorder, 1)
    return vx,vy

'''
    compute next position
'''
def compute_next_position(vx, vy, x, y, Ts):
    x = Ts*vx+x
    y = Ts*vy+y
    return x, y

'''
    compute next velocity
'''
def compute_next_velocity(vx, vy, ax, ay, Ts):
    vx = Ts*ax+vx
    vy = Ts*ay+vy
    return vx, vy


'''
    compute cumulative distance of trajectory
'''
def compute_cumulative_distance(x, y):
    dif_x = [(x[i+1]-x[i])**2 for i in range(0, len(x)-1)]
    dif_y = [(y[i+1]-y[i])**2 for i in range(0, len(y)-1)]
    distances=[np.sqrt(dif_x[i]+dif_y[i]) for i in range(0, len(dif_x))]
    total_distance=np.sum(distances)
    return total_distance

