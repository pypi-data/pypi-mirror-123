#!/usr/bin/env python
from main_pkg import *

print("=========root main========")
print(__name__)
print("==========================")

# eğer hazırladığımız paket aynı zamanda kend ibaşına çalışan bir uygulama ise kullanılır. 
# doğrudan çalıştırıldığında uygulamanın ayağa kalması için gerekli kodlar buradan başlatılır
if __name__ == "__main__":
    main_module.main_fonksiyon()