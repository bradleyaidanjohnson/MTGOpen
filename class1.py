import class2
    
class Default_Class:
    def __init__(self,name):
        self.name = name
    def enters_the_battlefield(self, **kwargs):
        if kwargs:
            kwargs['func'](self)
        print(f"{self.name} has entered the battlefield")

def Hello():
    print("hello")

a = Default_Class('a')

a.enters_the_battlefield()

a.enters_the_battlefield(func=class2.Cavern_of_Souls)