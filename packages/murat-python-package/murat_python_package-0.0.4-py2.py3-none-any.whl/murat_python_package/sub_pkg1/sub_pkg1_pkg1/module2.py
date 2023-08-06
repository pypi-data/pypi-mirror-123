__all__ = ["fonksiyon","Module2Class1"]
# bu modülü import edecek olan dosyanın impoert emesi gereken nesneler
# python 3.2 ve üstü için lazım

def fonksiyon():
    print ("ben modul2")
class Module2Class1:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "sub_pkg1 atında sub_pkg1_pkg1 altında Module2 altındaki Module2Class1 classıyım. Runtime Adım:" + __name__
    
    def name_getir(self):
        return self.name

print(__name__ + " yüklendi")
