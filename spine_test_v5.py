import maya.cmds as cmds
import logging
logger = logging.getLogger(__name__)

import rig_class.spine_data as sd

#self.temp_joint = attribute / not passing arguments.
#minimize the num of arguments / replace with data


class SpineRig(object):
    def __init__(self, spine_data):
        self.spine_data = sd.SpineData()


    def create_sample(self):
        '''
        Description:
            Creates temporary spine joint chain.
        Parameters:
            jntNum = number of joints.
            jntNum = spine_data.num_jnt
        Returns:
            A list of temporary joints.
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
        Parameters:
            temp = sample_jnt_list from create_sample or spine_data.sample_rig_jnt
            name = spine_data.cha_naming
        Returns:
            A list of final joints.
        '''
        self.spine_data.final_jnt_list = list()
        num = 1
        cmds.select(cl=True)

        temp = self.spine_data.temp_jnt_list
        name = self.spine_data.cha_naming

        logging.info('Before final_jnt_list Updates :{}'.format(self.spine_data))

        for tempJnt in temp:
            transVar = cmds.xform(tempJnt, worldSpace = True, query = True, translation = True)
            skin_j_startnt = cmds.joint(n = '{}_spine_{}_jnt'.format(name, num), absolute = True, position = transVar)
            self.spine_data.final_jnt_list.append(skin_j_startnt)
            num = num + 1

        for finalJnt in self.spine_data.final_jnt_list:
            cmds.joint(finalJnt, e=True, oj='xyz', secondaryAxisOrient = 'yup', ch=True, zso=True)

        endJnt = self.spine_data.final_jnt_list[-1]
        cmds.setAttr('{}.jointOrientX'.format(endJnt), 0)
        cmds.setAttr('{}.jointOrientY'.format(endJnt), 0)
        cmds.setAttr('{}.jointOrientZ'.format(endJnt), 0)


        logging.info('After final_jnt_list Updates :{}'.format(self.spine_data))


    def create_group(self, target):
        name = '{}_ctl_grp'.format(target)
        group_product = cmds.group(n = name, em=True)
        return group_product


    def create_control(self, target):
        name = '{}_ctl'.format(target)
        ctl_pair = list()

        ctl = cmds.circle(n = name, r=5, nr=(1,0,0))
        ctl_grp = self.create_group(target)

        #  Warning: Cannot parent components or objects in the underworld.
        cmds.parent(ctl, ctl_grp)

        ctl_pair.append(ctl[0])
        ctl_pair.append(ctl_grp)


        return ctl_pair


    def constraints_objs(self, ctl, target):
        cmds.parentConstraint(ctl, target)



class FK_rig(SpineRig):

    def __init__(self, spine_data):
        super(FK_rig, self).__init__(self)
        self.spine_data = spine_data

    # Find a way to remove target argument. Create another list parameter?
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
        self.constraints_objs(ctl, target)

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

        print 'flag before parenting'

        for num in range(len(ctl_grp)):
            if num != 0:
                currentCtl = ctl_grp[num]#Find the current control
                currentGrp = cmds.listRelatives(currentCtl, parent=True)#Find the parent group of the current control.
                aboveCtl = ctl_grp[num-1]#Find the control before the current one.
                cmds.parent(currentGrp, aboveCtl)#Parent current control's parent group to the above control.
        print 'flag after parenting'



    def create_FK(self):
        '''
        Description:
            Creates FK spine.
        Returns:
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
        self.startJ = None
        self.endJ = None

    def create_ikHandle(self):
        # need first and end joint/ from final joint list
        # need create ik cmds options

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

        cmds.rename(self.ik_product[2], nameCuv)
        self.ik_product[2] = nameCuv

        logging.info('ik product: {}'.format(self.ik_product))


    def create_skin_jnt(self):
        #start, middle, end

        cmds.select(cl=True)

        skin_j_start = cmds.joint(n='{}_spine_con_1'.format(self.spine_data.cha_naming))
        cmds.matchTransform(skin_j_start , self.startJ, pos=True)

        skin_j_end = cmds.joint(n='{}_spine_con_1'.format(self.spine_data.cha_naming))
        cmds.matchTransform(skin_j_end , self.endJ, pos=True)



    def skin_jnt_to_curve(self):
        pass

    def create_IK(self):

        self.create_joint()

        self.create_ikHandle()

        self.create_skin_jnt()

        #create joints, skin them to the curve.