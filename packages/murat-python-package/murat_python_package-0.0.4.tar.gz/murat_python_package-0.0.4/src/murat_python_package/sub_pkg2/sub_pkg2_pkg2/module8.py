__all__ = ["fonksiyon","Module2Class1"]




def fonksiyon():
    print ("ben modul8")


class Module2Class1:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "sub_pkg2 atında sub_pkg2_pkg2 altında Module8 altındaki Module2Class1 classıyım. Runtime Adım:" + __name__
    
    def name_getir(self):
        return self.name

print(__name__ + " yüklendi")
