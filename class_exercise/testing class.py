#testing class
class Info():
    def __init__(self):
        pass

    def phrase(self):
        phrase = 'Our family name is'
        return phrase

    def name(self):
        name = 'Jones'
        return name

    #didn't work
    """
    def all(self, phrase()):
        a = self.phrase()
        b = self.name()
        formatting = '{} {}.'.format(a, b)
        print formatting
    """

class Introduction(Info):
    def __init__(self):
        super(Info, self).__init__(self)


    def all(self):
        a = self.phrase()
        b = self.name()
        formatting = '{} {}.'.format(a, b)
        print formatting

child = Introduction()
child.all()
#Raises TypeError: file <maya console> line 3: must be type, not classobj
#https://stackoverflow.com/questions/9698614/super-raises-typeerror-must-be-type-not-classobj-for-new-style-class



#Function in function??
def a_say():
    return 'lala'

def b_say():
    a = a_say()
    b = '{} lulu'.format(a)
    return b

print b_say()