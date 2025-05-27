import maya.cmds as cmds

from autoRigger import constant
from autoRigger.core.joint import Joint
from autoRigger.util import file, skeleton, transform, util

class Chain(Joint):

    def __init__(self, name='name', side='L', ctrlShape=['circle'], mirror=None, segments=3, direction=(1,0,0), distance=5, scale=1.0):
        '''Create a simple chain.
        Args:
            segments (int): amount of joints in the chain needed
            distance (float): the amount inbetween each joint'''
        super(Chain, self).__init__(name, side, ctrlShape, mirror, scale)

        self.segments = segments
        self.direction = direction
        self.distance = distance
        self.components= list()
        for index in range(self.segments):
            self.components.append(f'{self.name}_{index}')

    def create_locs(self):
        '''Creates locators based on the amount of items specified for the chain. Parents locators underneath each other'''
        for index in range(len(self.components)):
            cmds.spaceLocator(name=self.locs[index])
            transform.setLocScale(self.locs[index], self.scale)
            cmds.xform(t=(index*self.distance*self.scale,0,0))
            if index:
                cmds.parent(self.locs[index], self.locs[index-1])
        cmds.parent(self.locs[0], constant.GRP_LOCS)

    def create_joints(self):
        cmds.select(clear=True)
        for index in range(len(self.components)):
            cmds.joint(name=self.jnts[index])
            transform.match_translate(self.jnts[index], self.locs[index])
        skeleton.orient_joint(self.jnts, constant.JNT_ORIENT, constant.JNT_SAO)
        cmds.parent(self.jnts[0], constant.GRP_JNTS)

        #orient final joint
        cmds.select(clear=True)
        cmds.select(self.jnts[self.segments-1])
        cmds.joint(e=1, ch=1, oj='none', zso=1)

    def create_controller(self):
        return         