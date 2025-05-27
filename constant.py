import os

GRP_LOCS = '_Locators'
GRP_JNTS = '_Joints'
GRP_CTRLS = '_Controllers'
GRP_LIST=[GRP_LOCS,GRP_JNTS,GRP_CTRLS]
GRP_TEMP_CTRLS = 'TEMP_CONTROLLERS'

#orientation taken from the manny rig
JNT_ORIENT = 'xyz'
JNT_SAO = 'zdown'

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

UI_FOLDER = os.path.join(PROJECT_ROOT, 'ui')
UI_FILE = 'autoRigger.ui'