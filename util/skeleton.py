import maya.cmds as cmds

def set_preferred_angle(jnt, angle=[0,1,0]):
    '''Sets the preferred angle of a joint. Rotates the joint in the direction of the angle by an offset amount and then reverts it
    Args:
        jnt (str): the joint to set the preferred angle, usually elbow or knee joint of ik systems'''
    offset=45
    for index in range(len(angle)):
        angle[index]*=offset
    cmds.rotate(angle[0], angle[1], angle[2], jnt, relative=1)
    cmds.joint(jnt, edit=True, setPreferredAngles=True)
    cmds.rotate(angle[0]*-1, angle[1]*-1, angle[2]*-1, jnt, relative=1)

def mirrorLocs(side, locs):
    '''Mirrors locs over to the other side specified'''
    group= cmds.group(empty=True, name=f'TEMP_MIRROR')
    for loc in locs:
        cmds.parent(loc, group, absolute=True)
    cmds.scale(1,1,-1, group)
    
def mirrorJnts(jnts, search, replace):
    '''Mirrors joint, currently only searches and replaces suffixes, also only mirros across yz axis'''
    for jnt in jnts:
        if cmds.objExists(jnt.replace(search, replace)): #check if it already exists
            print(f'{jnt.replace(search, replace)} already exists')
        else:
            print(f'Creating {jnt.replace(search, replace)}')
            cmds.mirrorJoint(jnt, mirrorBehavior=True,myz=True, searchReplace=(search, replace))

def orient_joint(jnts, orient, sao):
    '''Orients a chain of joints to the orientation specified.
    Args: 
        jnts (list): list of joints you wish to orient
        orient (str): the orientation you want. This can be xyz, yzx, zxy, zyx, yxz, xzy, or none. The first letter in the argument will be aligned with the vector from the joint to its child. The other two are dependent on sao is used
        sao (str): the secondary axis orientation. Can be xup, xdown, yup, ydown, zup, zdown, none.
    '''
    cmds.select(clear=True)
    for jnt in jnts:
        cmds.select(jnt, add=1)
    
    cmds.joint(e=1, ch=1, oj=orient, sao=sao)