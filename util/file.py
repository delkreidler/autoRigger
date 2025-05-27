import maya.cmds as cmds
import os

from autoRigger import constant

def import_files(fileName):
    '''Imports objects from a maya file. Raises error if file does not exist.
    Args:
        fileName (str): file name you wish to import
    '''
    try:
        filePath= os.path.join(constant.FOLDER_CURVES, fileName)
        cmds.file(filePath, i=True)
    except RuntimeError as e:
        print(f'Warning: Files was not found. Error: {e}')
    except:
        print('Unknown Error occurred during import file.')

def import_curve_files(curveList):
    '''Imports curve files and groups them underneath one group for easier cleanup
    Args: 
        curveList (list): list of names for the curves you want. The .ma will be added automatically
    '''
    if not cmds.objExists(constant.GRP_TEMP_CTRLS):
        group=cmds.group(empty=1, name=constant.GRP_TEMP_CTRLS)
    for curve in curveList:
        if curve == None:
            continue
        if cmds.objExists(curve):
            continue
        curveFile= curve+'.ma'
        import_files(curveFile)
        cmds.parent(curve,constant.GRP_TEMP_CTRLS)