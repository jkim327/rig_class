import maya.cmds as cmds
import maya.mel as mel
import logging
logger = logging.getLogger(__name__)

import rig_class.spine_data as sd

class SpineRig(object):
    def __init__(self, spine_data):
        self.spine_data = sd.SpineData()


    def create_sample(self):
        '''
        Description:
            Creates temporary spine joint chain.
        Returns:
            spine_data updates
        '''
        logging.info('Before temp_jnt_list Updates :{}'.format(self.spine_data)) #it has correct dic

        startTemp = 'spine_0_temp_jnt'

        if cmds.objExists(startTemp):
            cmds.delete(startTemp)

        trsY = 10

        self.spine_data.temp_jnt_list = list()

        for num in range(self.spine_data.num_jnt):
            if num == 0:
                new_jnt = cmds.joint(n='spine_{}_temp_jnt'.format(num))
                self.spine_data.temp_jnt_list.append(new_jnt)

            else:
                new_jnt = cmds.joint(n='spine_{}_temp_jnt'.format(num),position = [0, trsY*num, 0])
                self.spine_data.temp_jnt_list.append(new_jnt)

        logging.info('After temp_jnt_list Updates :{}'.format(self.spine_data))



    def create_joint(self):
        '''
        Description:
            Creates final spine joint chain.
        Returns:
            spine_data updates
                a list of final joints.
        '''
        self.spine_data.final_jnt_list = list()
        num = 1
        cmds.select(cl=True)

        temp = self.spine_data.temp_jnt_list
        name = self.spine_data.cha_naming

        logging.info('Before final_jnt_list Updates :{}'.format(self.spine_data))

        for tempJnt in temp:
            transVar = cmds.xform(tempJnt, worldSpace = True, query = True, translation = True)
            new_rig_jnt = cmds.joint(n = '{}_spine_{}_jnt'.format(name, num), absolute = True, position = transVar)
            self.spine_data.final_jnt_list.append(new_rig_jnt)
            num = num + 1

        for finalJnt in self.spine_data.final_jnt_list:
            cmds.joint(finalJnt, e=True, oj='xyz', secondaryAxisOrient = 'yup', ch=True, zso=True)

        #clean the end joint's orientation
        endJnt = self.spine_data.final_jnt_list[-1]
        cmds.setAttr('{}.jointOrientX'.format(endJnt), 0)
        cmds.setAttr('{}.jointOrientY'.format(endJnt), 0)
        cmds.setAttr('{}.jointOrientZ'.format(endJnt), 0)

        logging.info('After final_jnt_list Updates :{}'.format(self.spine_data))



    def create_control(self, target):
        '''
        Description:
            Creates nurbs curve controller and its parent group.
        Parameters:
            target
        Returns:
            a list of nurbs curve and its parent group
        '''
        name = '{}_ctl'.format(target)
        ctl_pair = list()

        if self.spine_data.fk_rig == True:
            ctl = create_circle(name)

        elif self.spine_data.ik_rig == True:
            ctl = create_box(name)

        ctl_grp = create_group(ctl)

        #  Warning: Cannot parent components or objects in the underworld.
        cmds.parent(ctl, ctl_grp)

        ctl_pair.append(ctl)
        ctl_pair.append(ctl_grp)

        return ctl_pair




class FK_rig(SpineRig):

    def __init__(self, spine_data):
        super(FK_rig, self).__init__(self)
        self.spine_data = spine_data

    def create_FK_con(self, target):
        '''
        Description:
            Creates FK controllers.
        Parameters:
            target = single final joint
        Returns:
            ctl string
        '''
        pair = self.create_control(target)#return list of a pair (ctl and ctl grp)
        ctl, ctl_grp = pair

        cmds.matchTransform(ctl_grp, target)
        constraints_objs(ctl, target)

        self.spine_data.ctl_list.append(ctl)

        return ctl


    def organize_fk(self):
        '''
        Description:
            Parent fk controllers in order.
        Returns:
            None
        '''

        ctl_grp = self.spine_data.ctl_list

        for num in range(len(ctl_grp)):
            if num != 0:
                currentCtl = ctl_grp[num]#Find the current control
                currentGrp = cmds.listRelatives(currentCtl, parent=True)#Find the parent group of the current control.
                aboveCtl = ctl_grp[num-1]#Find the control before the current one.
                cmds.parent(currentGrp, aboveCtl)#Parent current control's parent group to the above control.



    def create_FK(self):
        '''
        Description:
            Creates FK spine.
        Returns:
            spine_data updates
                Final joints
                FK controllers
        '''

        temp_jnts = self.spine_data.temp_jnt_list[0]

        #If temporary joints does not exists, stop the process.
        if not cmds.objExists(temp_jnts):
            return logging.error('Temporary joints not exist.')

        #create final joints
        self.create_joint()

        #clear list
        self.spine_data.ctl_list = list()

        #create controllers
        for jnt in self.spine_data.final_jnt_list:
            self.create_FK_con(jnt)

        #organize hierarchy
        self.organize_fk()
        logging.info('fk controls update {}'.format(self.spine_data))




class IK_rig(SpineRig):

    def __init__(self, spine_data):
        super(IK_rig, self).__init__(self)
        self.spine_data = spine_data
        self.ik_product = list()
        self.skin_jnt = list()
        self.fk_jnt = list()
        self.startJ = None
        self.endJ = None


    def create_ikHandle(self):
        '''
        Description:
            Creates ik Spline Handle
        Returns:
            self.ik_product updates
                ikHandle, curve object
        '''
        self.startJ = self.spine_data.final_jnt_list[0]
        self.endJ = self.spine_data.final_jnt_list[-1]

        nameIkh = '{}_spine_ikh'.format(self.spine_data.cha_naming)
        nameCuv = '{}_spine_cuv'.format(self.spine_data.cha_naming)

        self.ik_product = cmds.ikHandle(solver='ikSplineSolver',
                                        ccv = True,
                                        n = nameIkh,
                                        parentCurve = True,
                                        rootOnCurve = True,
                                        scv = False,
                                        ns = 4,
                                        sj = self.startJ,
                                        ee = self.endJ)

        #rename newly created curve
        cmds.rename(self.ik_product[2], nameCuv)
        self.ik_product[2] = nameCuv

        logging.info('ik product: {}'.format(self.ik_product))


    def set_twist(self):
        '''
        Description:
            set ikSplineHandle's twist setting.
        Returns:
            None
        '''

        ik_Handle = self.ik_product[0]

        cmds.setAttr(ik_Handle +'.dTwistControlEnable', True)
        cmds.setAttr(ik_Handle +'.dWorldUpType', 4)
        cmds.setAttr(ik_Handle +'.dWorldUpAxis', 0)

        cmds.connectAttr(self.skin_jnt[0]+'.worldMatrix[0]', ik_Handle +'.dWorldUpMatrix' )
        cmds.connectAttr(self.skin_jnt[-1]+'.worldMatrix[0]', ik_Handle +'.dWorldUpMatrixEnd' )


    def manage_skin_jnt(self):
        '''
        Description:
            Creates ik Spline Handle
        Returns:
            self.ik_product updates
                ikHandle, curve object
        '''

        self.skin_jnt = list()

        skin_start_j = create_skin_jnt(self.startJ, 'root')
        skin_end_j = create_skin_jnt(self.endJ, 'chest')

        self.skin_jnt.append(skin_start_j)
        self.skin_jnt.append(skin_end_j)


    def skin_jnt_to_curve(self):
        '''
        Description:
            Skin newly created self.skin_jnt to ikhandle curve.
        Returns:
            None
        '''
        cmds.skinCluster(self.skin_jnt, self.ik_product[2], mi=3)


    def create_fk_chain(self):
        '''
        Description:
            Create waist FK joint.
        Returns:
            self.fk_jnt updates
        '''
        all_num = len(self.spine_data.final_jnt_list)

        if all_num % 2 == 0:
            mid_num = all_num/2-1
        else:
            mid_num = all_num/2

        fk_goal_jnts = [self.spine_data.final_jnt_list[0], self.spine_data.final_jnt_list[mid_num], self.spine_data.final_jnt_list[-1]]
        fk_part_name = ['root', 'waist', 'chest']

        cmds.select(cl=True)

        for num in range(len(fk_goal_jnts)):
            jnt = fk_goal_jnts[num]
            part = fk_part_name[num]
            new_jnt = cmds.joint(n='{}_fk_jnt'.format(part))
            cmds.matchTransform(new_jnt, jnt)
            self.fk_jnt.append(new_jnt)


    def create_waist(self):
        '''
        Description:
            Create waist FK setting.
        Returns:
            None
        '''
        waist_jnt = self.fk_jnt[1]

        ctl_name = '{}_ctl'.format(waist_jnt)

        ctl = create_circle(ctl_name)
        ctl_grp = create_group(ctl)
        cmds.parent(ctl, ctl_grp)
        cmds.matchTransform(ctl_grp, waist_jnt, pos=True, rot=True)

        self.spine_data.ctl_list.append(ctl)

        constraints_objs(ctl, waist_jnt)


    def create_IK_con(self, target):
        '''
        Description:
            Creates IK controllers.
        Parameters:
            target = single final joint
        Returns:
            ctl string
        '''
        pair = self.create_control(target)#return list of a pair (ctl and ctl grp)
        ctl, ctl_grp = pair

        cmds.matchTransform(ctl_grp, target)

        # find target joint's parent group
        target_parent = cmds.listRelatives(target, parent=True)

        constraints_objs(ctl, target)

        self.spine_data.ctl_list.append(ctl)

        return ctl


    def organize_ik(self):
        '''
        Description:
            Constraints IK controllers in order.
        Returns:
            None
        '''
        waist_con = self.spine_data.ctl_list[-1]
        chest_con = self.spine_data.ctl_list[1]
        root_con = self.spine_data.ctl_list[0]

        fk_end_jnt = self.fk_jnt[0]

        chest_grp = cmds.listRelatives(chest_con, parent=True)
        waist_grp = cmds.listRelatives(waist_con, parent=True)

        constraints_objs(waist_con, chest_grp)
        constraints_objs(root_con, waist_grp)
        constraints_objs(root_con, fk_end_jnt)


    def create_IK(self):
        '''
        Description:
            Create IK Spine objects.
        Returns:
            None
        '''
        self.create_joint()

        self.create_ikHandle()

        self.manage_skin_jnt()

        self.skin_jnt_to_curve()

        self.set_twist()

        for jnt in self.skin_jnt:
            self.create_IK_con(jnt)

        self.create_fk_chain()

        self.create_waist()

        self.organize_ik()



#  Outside Class Functions
def create_group(target):
    '''
    Description:
        Creates parent group of the target object.
    Parameters:
        target
    Returns:
        newly created parent group
    '''
    name = '{}_grp'.format(target)
    group_product = cmds.group(n = name, em=True)

    return group_product


def create_circle(name):
    '''
    Description:
        Creates nurbs circle with name.
    Parameters:
        name string
    Returns:
        newly created nurbs circle's name
    '''
    circle = cmds.circle(n = name, r=5, nr=(1,0,0))
    return circle[0]

def create_box(name):
    '''
    Description:
        Creates nurbs cube with name.
    Parameters:
        name string
    Returns:
        newly created nurbs cube's name
    '''
    box = cmds.curve(n = name, d=1, p=[(2.5, 2.5, 2.5), (2.5, 2.5, -2.5), (-2.5, 2.5, -2.5), (-2.5, -2.5, -2.5), (2.5, -2.5, -2.5), (2.5, 2.5, -2.5), (-2.5, 2.5, -2.5), (-2.5, 2.5, 2.5), (2.5, 2.5, 2.5), (2.5, -2.5, 2.5), (2.5, -2.5, -2.5), (-2.5, -2.5, -2.5), (-2.5, -2.5, 2.5), (2.5, -2.5, 2.5), (-2.5, -2.5, 2.5), (-2.5, 2.5, 2.5)], k=[0,1,2,3,4,2.5,7,8,9,10,11,12,13,14,12.5,16])
    return box

def constraints_objs(ctl, target):
    cmds.parentConstraint(ctl, target, mo=True)


def create_skin_jnt(target, name):#receives self.startJ, self.endJ
    '''
    Description:
        Creates extra joint chain for curve skinning.
    Parameters:
        target = target joint
        name
    Returns:
        newly created joint's name
    '''
    cmds.select(cl=True)

    new_joint = cmds.joint(n='{}_skin_jnt'.format(name))
    new_joint_grp = create_group(new_joint)

    cmds.parent(new_joint, new_joint_grp)
    cmds.matchTransform(new_joint_grp, target, pos=True, rot=True)

    return new_joint
