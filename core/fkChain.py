import maya.cmds as cmds

from autoRigger import constant
from autoRigger.core.chain import Chain
from autoRigger.util import util, transform, file, shape

class FKChain(Chain):
    def __init__(self, name='name', side='L', ctrlShape=['circle'], mirror=None, segments=3, direction=(1,0,0), distance=5, scale=1.0):
        super(FKChain, self).__init__(name, side, ctrlShape, mirror, segments, direction, distance, scale)

    def construct_names(self):
        '''Creates the names of all locators, joints, and controllers based on the components'''
        for index in range(len(self.components)):
            self.locs.append(util.name_guide(name=self.components[index], side=self.side, type='loc'))
            self.jnts.append(util.name_guide(name=self.components[index], side=self.side, type='jnt', variant='fk'))
            self.ctrls.append(util.name_guide(name=self.components[index], side=self.side, type='ctrl', variant='fk'))
            self.ctrlsGRP.append(util.name_guide(name=self.components[index], side=self.side, type='ctrlGRP', variant='fk'))

    def create_controller(self):
        for index in range(len(self.components)):
            ctrlShape = self.ctrlShape[0]
            name = self.ctrls[index]
            shape.curveShapes[ctrlShape](name = name)
            transform.setObjScale(self.ctrls[index], self.scale)
            group=cmds.group(empty=1, name=f'{self.ctrlsGRP[index]}')
            cmds.parent(self.ctrls[index], group)
            if index:
                cmds.parent(group, self.ctrls[index-1])
            cmds.matchTransform(group, self.jnts[index])
            cmds.parentConstraint(self.ctrls[index], self.jnts[index], maintainOffset=True) 
        cmds.parent(self.ctrlsGRP[0], constant.GRP_CTRLS)