import numpy as np
import astarwrapper
from time import time

def fpath(grid):

    grid[grid == 9] = np.inf

    start = np.argwhere(grid==2)[0]

    end = np.argwhere(grid==3)[0]

    t0 = time()

    path = astarwrapper.astar_path(grid, start, end)

    if path.shape[0] > 0:
        print('found path of length %d' % (path.shape[0]))
        path=np.insert(path, 0, start, axis=0)
        # print(path)
    else:
        print('no path found')


    moves=[]

    current_orientation = -1
    
    stop=[False,0]
    
    for i in range(len(path)-1):
        x1=path[i][0]
        y1=path[i][1]
        x2=path[i+1][0]
        y2=path[i+1][1]
        
        if abs(x1-x2)==abs(y1-y2):

            if x1-x2<0 and y1-y2<0:
                orientation=2
                if orientation==current_orientation:
                    moves.append([True,0])
                else:
                    angle=45*(current_orientation-orientation)
                    current_orientation=orientation
                    moves.append([False,angle])
                    moves.append([True,0])
                continue

            elif x1-x2>0 and y1-y2<0:
                orientation=0
                if orientation==current_orientation:
                    moves.append([True,0])
                else:
                    angle=45*(current_orientation-orientation)
                    current_orientation=orientation
                    moves.append([False,angle])
                    moves.append([True,0])
                continue

            elif x1-x2<0 and y1-y2>0:
                orientation=4
                if orientation==current_orientation:
                    moves.append([True,0])
                else:
                    angle=45*(current_orientation-orientation)
                    current_orientation=orientation
                    moves.append([False,angle])
                    moves.append([True,0])
                continue

            elif x1-x2>0 and y1-y2>0:
                orientation=-2
                if orientation==current_orientation:
                    moves.append([True,0])
                else:
                    angle=45*(current_orientation-orientation)
                    current_orientation=orientation
                    moves.append([False,angle])
                    moves.append([True,0])
                continue

        elif x2==x1 and y2>y1:
            orientation=1
            if orientation==current_orientation:
                moves.append([True,0])
            else:
                angle=45*(current_orientation-orientation)
                current_orientation=orientation
                moves.append([False,angle])
                moves.append([True,0])
            continue

        elif x2==x1 and y2<y1:
            orientation=5
            if orientation==current_orientation:
                moves.append([True,0])
            else:
                angle=45*(current_orientation-orientation)
                current_orientation=orientation
                moves.append([False,angle])
                moves.append([True,0])
            continue
        
        elif y2==y1 and x2>x1:
            orientation=3
            if orientation==current_orientation:
                moves.append([True,0])
            else:
                angle=45*(current_orientation-orientation)
                current_orientation=orientation
                moves.append([False,angle])
                moves.append([True,0])
            continue

        elif y2==y1 and x2<x1:
            orientation=-1
            if orientation==current_orientation:
                moves.append([True,0])
            else:
                angle=45*(current_orientation-orientation)                
                current_orientation=orientation
                moves.append([False,angle])
                moves.append([True,0])
            continue

    print(moves)
    dur = time() - t0
    print(dur)
    return moves

if __name__ == '__main__':
    fpath(grid= np.array([[ 2., 0., 0., 0.],
                    [ 0., 0., 3., 0.],
                    [ 0., 0., 0., 0.]], dtype=np.float32))
