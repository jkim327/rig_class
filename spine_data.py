class SpineData():

    def __init__(self,
                 num_jnt = None,
                 fk_rig = False,
                 ik_rig = False,
                 temp_jnt_list = list(),
                 final_jnt_list = list(),
                 cha_naming = None,
                 ctl_list = list(),
                 ):
        self.num_jnt = num_jnt
        self.fk_rig = fk_rig
        self.ik_rig = ik_rig
        self.temp_jnt_list = temp_jnt_list
        self.final_jnt_list = final_jnt_list
        self.cha_naming = cha_naming
        self.ctl_list = ctl_list

        self.data = self.__dict__

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return "{}: {}, {}, {}, {}".format(
            self.__class__.__name__,
            self.num_jnt,
            self.fk_rig,
            self.ik_rig,
            self.cha_naming,
            )