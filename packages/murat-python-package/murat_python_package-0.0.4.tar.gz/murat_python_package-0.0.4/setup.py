# setuptool modülü için script oluşturur.
# setupçpy dynamic bir yapıdadır. setap yaplırken kod blokları çalıştırılabilir
# birde setup.cfg var bu da statik bir yapı sunar. statik bilgiler içindir. 
# mesela alttaki birçok bilgi aslında bu static setup.cfg dosyasında tutulabilir.
import pathlib
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

HERE = pathlib.Path(__file__).parent
LONG_DESCRIPTION = (HERE / "README.md").read_text()
setup(
    name="murat_python_package",
    version="0.0.4",
    author="Murat Çabuk",
    author_email="mcabuk@gmail.com",
    description="A small example package",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/muratcabuk/murat_python_package",
    project_urls={
        "Bug Tracker": "https://github.com/muratcabuk/murat_python_package/issues",
    },
    # python pypi da gecen kategoriler
    # https://pypi.org/classifiers/
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src",exclude=("tests",)),
    python_requires=">=3.6",
    options={"bdist_wheel": {"universal": "1"}},
    entry_points={
        'console_scripts': [
            'murat_python_package = murat_python_package.main_pkg.main_module:main_fonksiyon',
        ],
    },


)