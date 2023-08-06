from main_pkg import main_module
 



# eğer hazırladığımız paket aynı zamanda kend ibaşına çalışan bir uygulama ise kullanılır. 
# doğrudan çalıştırıldığında uygulamanın ayağa kalması için gerekli kodlar buradan başlatılır
if __name__ == "__main__":
    main_module.main_fonksiyon()