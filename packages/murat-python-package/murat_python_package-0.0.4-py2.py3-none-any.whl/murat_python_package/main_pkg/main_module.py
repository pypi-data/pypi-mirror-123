#!/usr/bin/env python
import click

import sys
sys.path.append("..") 
# main_pkg ile sub_pk1 ve sub_pkg2 aynı diznde oldukları için 
# root fonksiyondan diğer paket eklenmiyor bunun için bu path eklendi

print("========main_module main=========")
print(__name__)
print("=================")

if(__name__ == "murat_python_package.main_pkg.main_module"):
    from ..sub_pkg1.sub_pkg1_pkg1 import module1
elif (__name__ == "__main__"):
    raise Exception("Bu module doğrudan çağrılamaz")
else:
    from sub_pkg1.sub_pkg1_pkg1 import module1





__all__ =["main_fonksiyon"]

module1.fonksiyon()

print ("ben main_pkk paketi içindeki main_module üm")





@click.command()
@click.option('--isim', default="murat", help='mesaj verilecek kişi')
@click.option('--mesaj', default='Your name', help='isme verilecek mesaj')
def main_fonksiyon(isim:str, mesaj:str):
    """ISIM parametresinde verilen isme MESAJ parametresi ile verilen mesajı iletir"""
    click.echo(f"{mesaj}, {isim}")