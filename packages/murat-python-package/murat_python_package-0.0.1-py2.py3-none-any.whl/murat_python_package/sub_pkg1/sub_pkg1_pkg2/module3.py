__all__ = ["fonksiyon","Module1Class1"]
# bu modülü import edecek olan dosyanın impoert emesi gereken nesneler
# python 3.2 ve üstü için lazım


def fonksiyon():
    print ("ben modul3")


class Module1Class1:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "sub_pkg1 atında sub_pkg1_pkg2 altında Module3 altındaki Module1Class1 classıyım. Runtime Adım:" + __name__
    
    def name_getir(self):
        return self.name

print(__name__ + " yüklendi")
