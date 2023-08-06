# bu dosya konulmasa da olur çünki burada namespace package sistemini uyguluyoruz. 
# ancak python 3.2 ve üstü için lazım
# https://www.python.org/dev/peps/pep-0420/
# https://docs.python.org/3/reference/import.html#regular-packages


from .sub_pkg2_pkg1 import *
from .sub_pkg2_pkg2 import *

# __all__= ["module1","module2"]

__all__= ["module5","module6"] 
            # module8 sub_pkg2 paketi içinde 
            # sub_pkg2_pkg1 ve sub_pkg2_pkg2 paketleri içinde
            #  kullanılsın diye dışarı export edilmedi

            # module7 burada yazılmadı çünkü sub_pkg2_pk2 dışına export edilmedii için çalışmayacak
            
             
print(__name__ + " yüklendi")

