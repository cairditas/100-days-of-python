class Animal:
    def __init__(self):
        self.eyes = 3

    def breathe(self):
        print("Breathe")

class Dog(Animal):
    def __init__(self):
        super().__init__()

    def bark(self):
        print("Bark")


d = Dog()
d.breathe()
d.bark()