"""
1. call guide skeleton
2. receive guide skeleton information
3. create final skeleton
4. orient skeleton

Fk
5. create controls
6. position controls
7. constraint controls to skeleton
9. constraint controls

IK
5. create ik spline handle
6.
"""

import maya.cmds as cmds
logger = logging.getLogger(__name__)

class SpineRig(object):
    def __init__(self):
        pass

    def create_sample(self, jntNum):

        startTemp = 'spine_0_temp_jnt'
        if cmds.objExists(startTemp):
            cmds.delete(startTemp)
            logging.info('old sample has been deleted.')

        trsY = 10
        for num in range(jntNum):
            if num == 0:
                cmds.joint(n='spine_{}_temp_jnt'.format(num))
            else:
                cmds.joint(n='spine_{}_temp_jnt'.format(num),position = [0, trsY*num, 0])
        logging.info('Created a {}-joint chain.'.format(jntNum))

    def create_control(self, target):
        pass

class FK_rig(object):

    def __init__(self):
        pass

    def create_FK(self, temp, name):
        logging.info('FK spine has been selected')
        temp_list = temp
        jnt_list = []
        num = 1
        cmds.select(cl=True)

        for tempJnt in temp_list:
            print temp
            transVar = cmds.xform(tempJnt, worldSpace = True, query = True, translation = True)
            print transVar
            newJnt = cmds.joint(n = '{}_spine_{}_jnt'.format(name, num), absolute = True, position = transVar)
            jnt_list.append(newJnt)
            num = num + 1
