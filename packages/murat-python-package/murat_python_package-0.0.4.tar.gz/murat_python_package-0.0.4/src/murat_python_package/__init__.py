from .sub_pkg1 import *
from .sub_pkg2 import *
from .main_pkg import *


__all__ = ["module1","module2","module3","module4",
                "module5","module6"] 
                        # module7 ve 8 alta modullerde export edilmediği için burada kullanılmaz 

__version__ ="0.0.1"


print(__name__ + " yüklendi")


module1.fonksiyon()