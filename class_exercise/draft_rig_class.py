###########################
#Class for rigging in maya
#04.04.2020
#
#**Temporaility, the scope is limited to FK. (Ik will be added later)
###########################
import maya.cmds as cmds
import logging

"""
The general process of rigging.

1. Create Locators.(with name)
2. Place Locators.
3. Create Joints.(with name)
4. Replace locators with joints.
5. Orient Joints.
6. Create nurbs curve.(with name)
7. Create buffer nodes for the nurbs curves.(with name)
8. Match transformation nurbs curves to joints.
9. Constraint nurbs curves to joints.
10. Constraint nurbs curves in hierarchy.
+ Duplicate objects.
+ Search and Replace names. or Rename.

Get information of the object.
Create the object with proper name.
"""

#Class for Naming
class NamingComp(object):
    """
    Dictionary of naming components.
    Keys = [side, limb_name, object_type]

    The function uses the values to rename objects.
    """
    def __init__(self, side, limb, function, obj_type):
        self.data = self.__dict__
        self.side = side
        self.limb = limb
        self.function = function
        self.obj_type = obj_type

    def name_dict(self, side, limb, obj_type):
        """
        example = {'side': 'lf',
                    'limb' : 'shoulder',
                    'function' : 'FK',
                    'obj_type' : 'jnt'}
        """
        obj_name_dic = {'side': side,
                        'limb': limb,
                        'function': function
                        'obj_type': obj_type}
        return obj_name_dic

    #Do we need name_dict? 
    def name_string(name_dict):
        side = name_dict.get('side')
        limb = name_dict.get('limb')
        function = name_dict.get('function')
        obj_type = name_dict.get('obj_type')

        name_str = '{}_{}_{}_{}'.format(side, limb, function, obj_type)

        return name_str


#Class for Object
class RigObjects(object):#NamingComp as well?
    """
    The function includes

    1. Creation -> cmds.spaceLocator, cmds.joint, cmds.nurbsCircle(temp)
    2. MatchTransform
    3. Constraint
    4. Create buffer nodes -> makie group, matchTransform, parenting?
    """
    def __init__(self, obj_kind):
        """
        obj_kind can be...
            spaceLocator
            joint
            group(empty=True)
            ....curve?
        """
        self.obj_kind = obj_kind

    def createObj(self, obj_kind):

        cmds.select(cl=True)#To avoid any error

        if obj_kind == 'locator':
            obj = cmds.spaceLocator()
        elif obj_kind == 'joint':
            obj = cmds.joint()
        elif obj_kind == 'empty group':
            obj = cmds.group(empty=True)

        return object

    #testing_class file
    #
    def renameObj(self, new_name):
        """
        Rename the object with new naming combination.
        """
        name = new_name
        cmds.select(self)
        cmds.rename(self, name)

    def getPos(self):
        """
        Get object's position values
        """

    def matchTrs(self, source):
        '''
        Description:
            Match transformation both rotation and position.
        Parameters:
            source
        Returns:
            None
        '''
        cmds.matchTransform(self, source, position=True, rotation=True)

    def parentObj(self, source):
        """
        parenting
        """
    # getPos, matchTrs, parentObj -> can create joint at locator's positiong and parent them. + orienting
    # Should I..make a class for Joint as well?.....
    # createBuff also can be divided into smaller pieces... i think...
        def createBuff(self):
        '''
        Description:
            Create a buffer node and a locator between the parent node and the actual object.
        Parameters:
            None
        Returns:
            The first buffer node.
        '''
        nameGrp = '{}_buf_grp'.format(self)
        nameLoc = '{}_loc'.format(self)

        parentGrp = cmds.listRelatives(self, parent=True)

        # cmds.group -> RigObjects.createObj(obj_kind='empty group')?
        buffGrp = cmds.group(n=nameGrp,empty=True)
        buffLoc = cmds.spaceLocator(n=nameLoc)

        cmds.matchTransform(locA, sel, position=True, rotation=True)
        cmds.matchTransform(buffLoc, sel, position=True, rotation=True)
        cmds.parent(buffLoc, buffGrp)

        #For controllers, we assume it has at least one parent node for transform.
        If parentGrp != None:
            cmds.parent(buffGrp, parentGrp)
        else:
            pass
        cmds.parent(sel, buffLoc)

        return buffGrp



#Class for Joints
class FKObject(RigObjects):
    def __init__(self):
        super(RigObjects, self).__init__(self)

    def parentFKchain(self, buff_list):#should buff_list also needs to be at __init__?
        """
        Description:
            ParentConstraints FK controls in order.
        Parameters:
            The list of controllers' first buffer groups.(RigObjects.createBuff())
        Returns:
            None
        """
        for num in range(len(ctl_parent_Grp)):
            if num == 0:#If the control is the first, the shoulder control, it doesn't have parent.
                pass
            else:#Other controls need parent.
                currentCtl = ctl_parent_Grp[num]#Find the current control
                currentrigGrp = pm.listRelatives(currentCtl, parent=True)#Find the parent group of the current control.

                aboveCtl = ctl_parent_Grp[num-1]#Find the control before the current one.
                pm.parent(currentrigGrp, aboveCtl)#Parent current control's parent group to the above control.
                #This parents the fk controls in right order.








