import maya.cmds as cmds

from autoRigger import constant
from autoRigger.util import transform, file, util, shape

class Joint():
    '''Class for creating a single Joint. Includes construction of locator guides and construction of controllers'''
    def __init__(self, name='joint', side='L', ctrlShape=['circle'], mirror=None, scale=1.0):
        '''Creates the groups first and initializes variables
        ARGS:
            name (str): name of the joint
            side (str): either L, R, or M. To determine which side the joint will be on.
            ctrlShape (list): list of controller shapes to be imported
            mirror (str): which direction to mirror the joint'''
        self.create_groups()
        self.name = name
        self.side = side
        self.ctrlShape = ctrlShape
        self.mirror = mirror
        self.scale = scale

        self.locs=list()
        self.jnts=list()
        self.ctrls=list()
        self.ctrlsGRP=list()
        self.components=[self.name]
            
    def create_groups(self):
        '''Create groups to store locators, joints, and controllers'''
        for group in constant.GRP_LIST:
            if not cmds.objExists(group):
                cmds.group(empty=1, name=group)

    def create_locs(self):
        '''Create locators to be used as guides for the rig'''
        for index in range(len(self.components)):
            cmds.spaceLocator(name=self.locs[index])
            transform.setLocScale(self.locs[index], self.scale)
        cmds.parent(self.locs[0], constant.GRP_LOCS)

    def create_joints(self):
        '''Create joint based on placement of locator guides'''
        for index in range(len(self.components)):
            cmds.joint(name=self.jnts[index])
            transform.match_translate(self.jnts[index], self.locs[index])

        cmds.parent(self.jnts[0], constant.GRP_JNTS)

    def create_controller(self):
        '''Create the controller for the joint. Imports controller based on given controller name'''
        for index in range(len(self.components)):
            ctrlShape = self.ctrlShape[index]
            name = self.ctrls[index]
            shape.curveShapes[ctrlShape](name = name)
            transform.setObjScale(self.ctrls[index], self.scale)
            group=cmds.group(empty=1, name=f'{self.ctrlsGRP[index]}')
            cmds.parent(self.ctrls[index], group)
            cmds.matchTransform(group, self.jnts[index])
            cmds.parentConstraint(self.ctrls[index], self.jnts[index], maintainOffset=True) 
        cmds.parent(self.ctrlsGRP[0], constant.GRP_CTRLS)

    def delete_locs(self):
        '''Delete all Locator guides to clean up the scene'''
        for index in range(len(self.components)):
            if cmds.objExists(self.locs[index]):
                cmds.delete(self.locs[index])

    def color_nodes(self, nodes):
        '''Colors locator based on the side. Left is blue, right is red, middle is yellow
        Args:
            nodes (list): list of either locators or curves to color
            '''
        for item in nodes:
            if self.side == 'L':
                util.override_color(item, 0,0,1)
            elif self.side == 'R':
                util.override_color(item, 1,0,0)
            elif self.side == 'M':
                util.override_color(item, 0,0,1)
    
    def construct_names(self):
        '''Creates the names of all locators, joints, and controllers based on the components'''
        for index in range(len(self.components)):
            self.locs.append(util.name_guide(name=self.components[index],side=self.side, type='loc'))
            self.jnts.append(util.name_guide(name=self.components[index],side=self.side, type='jnt'))
            self.ctrls.append(util.name_guide(name=self.components[index],side=self.side, type='ctrl'))
            self.ctrlsGRP.append(util.name_guide(name=self.components[index],side=self.side, type='ctrlGRP'))

    def construct_guides(self):
        '''Creates guides for where the rig will be assembled'''
        self.construct_names()
        self.create_locs()
        self.color_nodes(self.locs)
    
    def construct_rig(self):
        '''Creates the rig from the position of the guides.'''
        self.create_joints()
        if self.mirror != None:
            cmds.mirrorJoint(self.jnts[0], mirrorBehavior=True, searchReplace=['L', 'R'])
        self.create_controller()
        if self.mirror != None:
            self.side= 'R'
            self.construct_names()
            self.create_controller()
        # self.delete_locs()
        transform.delete_temp_curves()