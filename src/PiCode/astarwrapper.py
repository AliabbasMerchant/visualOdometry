import ctypes
import numpy as np
from time import time

lib = ctypes.cdll.LoadLibrary('./astar.so')

astar = lib.astar
ndmat_f_type = np.ctypeslib.ndpointer(dtype=np.float32, ndim=1, flags='C_CONTIGUOUS')
ndmat_i_type = np.ctypeslib.ndpointer(dtype=np.int32, ndim=1, flags='C_CONTIGUOUS')

astar.argtypes = [ndmat_f_type, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ndmat_i_type]

def astar_path(grid, start, goal):
    
    height, width = grid.shape

    start_idx = np.ravel_multi_index(start, (height, width))
    goal_idx = np.ravel_multi_index(goal, (height, width))

    # The C++ so file writes the solution to the paths array
    paths = np.full(height * width, -1, dtype=np.int32)
    
    found = astar(grid.flatten(), height, width, start_idx, goal_idx, paths)
    
    if not found:
        return np.array([])

    coordinates = []
    path_idx = goal_idx
    
    while path_idx != start_idx:
        pi, pj = np.unravel_index(path_idx, (height, width))
        coordinates.append((pi, pj))
        path_idx = paths[path_idx]


    if coordinates:
        return np.vstack(coordinates[::-1])

    else:
        return np.array([])