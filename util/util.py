import maya.cmds as cmds

def name_guide(name=None, num=None, side=None, type=None, variant=None):
    '''Returns a string based on the naming conventions set here
    Args: 
        name (str): name of object
        side (str): l or r for left or right
        num (str): number of object
        type (str): loc, grp, jnt, or ctrl
        variant (str): fk, ik, or none
    '''
    stringList= [type, name, num, side, variant]
    resultString = ''
    for item in stringList:
        if item == None:
            continue
        elif resultString == '':
            resultString+=item
        else:
            resultString+=f'_{item}'
    return resultString

def override_color(node, r,g,b):
    '''Changes the viewport color of the given node. 
    Args:
        node (str): name of the node/locator/curve you want to change color. Make sure its the transform node and not the shape node
        r (int): normalized value for red
        g (int): normalized value for green
        b (int): normalized value for blue
    '''
    #check if the node is actually of transform type
    if cmds.nodeType(node) != 'transform':
        return

    cmds.setAttr(f'{node}.overrideEnabled', 1)
    cmds.setAttr(f'{node}.overrideRGBColors', 1)
    cmds.setAttr(f'{node}.overrideColorRGB', r,g,b)

def lock_and_hide(obj, t=False, r=True, s=True, v=True):
    '''Locks and Hides selected Attributes
    Args:
        obj (str): object name
        t (bool): locks and hides all translate attributes if true
        r (bool): locks and hides all rotate attributes if true
        s (bool): locks and hides all scale values
        v (bool): turns visibility on if true.
    '''
    if t:
        cmds.setAttr(obj+".translateX", l=True, k=False, cb=False)
        cmds.setAttr(obj+".translateY", l=True, k=False, cb=False)
        cmds.setAttr(obj+".translateZ", l=True, k=False, cb=False)
    if r:
        cmds.setAttr(obj+".rotateX", l=True, k=False, cb=False)
        cmds.setAttr(obj+".rotateY", l=True, k=False, cb=False)
        cmds.setAttr(obj+".rotateZ", l=True, k=False, cb=False)
    if s:
        cmds.setAttr(obj+".scaleX", l=True, k=False, cb=False)
        cmds.setAttr(obj+".scaleY", l=True, k=False, cb=False)
        cmds.setAttr(obj+".scaleZ", l=True, k=False, cb=False)
    if v:
        cmds.setAttr(obj+".visibility", l=True, k=False, cb=False)