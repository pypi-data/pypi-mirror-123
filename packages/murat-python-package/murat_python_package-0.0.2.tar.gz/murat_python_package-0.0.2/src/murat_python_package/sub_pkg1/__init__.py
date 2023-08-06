# bu dosya konulmasa da olur çünki burada namespace package sistemini uyguluyoruz. 
# ancak python 3.2 ve üstü için lazım
# https://www.python.org/dev/peps/pep-0420/
# https://docs.python.org/3/reference/import.html#regular-packages


from .sub_pkg1_pkg1 import * 
from .sub_pkg1_pkg2 import *

__all__= ["module1","module2","module3","module4"]

print(__name__ + " yüklendi")

