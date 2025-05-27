import maya.cmds as cmds

def nurbs_circle(name = 'name'):
    '''Creates a nurbs curve in the shape of a circle'''
    return cmds.circle( name = name, nr=(0, 0, 1), c=(0, 0, 0) )

def nurbs_square(name = 'name'):
    return cmds.nurbsSquare( name = name, nr=(0, 0, 1), d=1, c=(0, 0, 0), sl1=2, sl2=2 )

curveShapes = {
    'circle': nurbs_circle,
    'square': nurbs_square
}
