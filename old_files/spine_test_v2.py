import maya.cmds as cmds
import logging
logger = logging.getLogger(__name__)

import rig_class.spine_data as sd

class SpineRig(object):
    def __init__(self, spine_data):
        self.spine_data = sd.SpineData()
        self.temp_jnt_list = list()
        self.final_jnt_list = list()

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
        logging.info('Before Updates :{}'.format(self.spine_data)) #it has correct dic

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

        logging.info('After Updates :{}'.format(self.spine_data))



    #self.temp_joint = attribute / not passing arguments.
    #minimize the num of arguments / replace with data
    def create_joint(self, temp, name):
        '''
        Description:
            Creates final spine joint chain.
        Parameters:
            temp = sample_jnt_list from create_sample or spine_data.sample_rig_jnt
            name = spine_data.cha_naming
        Returns:
            A list of final joints.
        '''
        #temp = self.spine_data.sample_rig_jnt
        final_jnt_list = list()
        num = 1
        cmds.select(cl=True)

        for tempJnt in temp:
            transVar = cmds.xform(tempJnt, worldSpace = True, query = True, translation = True)
            newJnt = cmds.joint(n = '{}_spine_{}_jnt'.format(name, num), absolute = True, position = transVar)
            final_jnt_list.append(newJnt)
            num = num + 1

        self.final_jnt_list = final_jnt_list #init
        #return final_jnt_list #self.final_jnt_list


    def create_group(target):
        name = '{}_ctl_grp'.format(target)
        group_product = cmds.group(n = name, em=True)
        return group_product


    def create_control(target):
        name = '{}_ctl'.format(target)
        ctl_pair = list()

        ctl = cmds.circle(r=5, nr=(0,1,0))
        ctl_grp = self.create_group(target)
        cmds.parent(ctl, ctl_grp)
        ctl_pair.append(ctl)
        ctl_pair.append(ctl_grp)

        return ctl_pair



class FK_rig(SpineRig):

    def __init__(self):
        super(FK_rig, self).__init__()



    def create_FK_con(target):
        '''
        Description:
            Creates FK controllers.
        Parameters:
            target = single final joint
        Returns:
            A list of fk controllers and a list of controller groups.1
        '''
        pair = self.create_control(jnt)#return list of a pair (ctl and ctl grp)
        ctl, ctl_grp = pair

        cmds.matchTransform(ctl_grp, jnt)

        return ctl


    def connect_con_to_fkJnt(jnt, ctl):
        pass


    def create_FK(self, temp, name):
        '''
        Description:
            Creates FK spine.
        Parameters:
            temp = sample_jnt_list from create_sample or spine_data.sample_rig_jnt
            name = spine_data.cha_naming
        Returns:
            Updated data?
        '''
        new_jnts = self.create_joint(temp, name)
        return new_jnts

        ctl_list = list()

        #create FK controllers
        for jnt in new_jnts:
            ctl = self.create_FK_con(jnt)
            ctl_list.append(ctl)

        #connect controlloers and joints
        #(ctl, jnt)pair..... set...?.....



class IK_rig(FK_rig):
    """
    1. create IK spline handle.
    2. combine FK rig and spline rig....?
    """
    def __init__(self):
        super(IK_rig, self).__init__()

    def create_IK(self):
        pass
