import maya.cmds as cmds
from autoRigger import constant

def offset_position(obj, offset=[0,0,0]):
    '''Offsets an objects position based on given values
    Args:
        obj (str): the object you want to transform
        offset (list): 3 value list for the offset value you want'''
    pos = cmds.xform(obj, q=1, t=1, ws=1) #get the translation values
    newpos=[]
    for index in range(len(offset)):
        newpos.append(pos[index]+offset[index])

    cmds.move(newpos[0], newpos[1], newpos[2], obj)   #add to existing values

def setObjScale(obj, scale):
    '''Sets the objects scale and freezes transforms'''
    cmds.scale(scale, scale, scale, obj)
    cmds.makeIdentity(obj, apply=True )

def setLocScale(loc, scale):
    '''Sets the locators scale'''
    cmds.setAttr(loc+'.localScaleX', scale)
    cmds.setAttr(loc+'.localScaleY', scale)
    cmds.setAttr(loc+'.localScaleZ', scale)

def match_translate(source, target):
    '''Matches the sources translation to the target
    Args:
        source (str): the object you want to apply the xforms to
        target (str): the object you want to copy from
    '''
    pos = cmds.xform(target, q=1, t=1, ws=1)
    cmds.move(pos[0], pos[1], pos[2], source)


def delete_temp_curves():
    '''Deletes the temp curves folder if it exists'''
    if cmds.objExists(constant.GRP_TEMP_CTRLS):
        cmds.delete(constant.GRP_TEMP_CTRLS)