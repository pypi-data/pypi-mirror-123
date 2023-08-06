import io
from pathlib import Path

from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import find_packages, setup

__version__ = "0.0.1"


def read_files(files):
    data = []
    for file in files:
        with io.open(file, encoding="utf-8") as f:
            data.append(f.read())
    return "\n".join(data)


silk_source_list = [
    str(file.resolve())
    for file in Path('src/silk/src').iterdir()
    if file.suffix == '.c'
]

ext_modules = [
    Pybind11Extension(
        "_pysilk",
        ["src/_pysilk.cpp", "src/codec.cpp", *silk_source_list],
        include_dirs=["src/silk/interface", "src/silk/src"],
        define_macros=[("VERSION_INFO", __version__)],
    )
]

setup(
    name="python-silk",
    version=__version__,
    author="DCZYewen",
    author_email="contact@basicws.net",
    url="https://github.com/DCZYewen/Python-Silk-Module",
    description="Python silk decode/encoder bindings using pybind11",
    long_description=read_files(['README.md']),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    ext_modules=ext_modules,  # type: ignore
    extras_require={"test": "pytest"},
    setup_requires=["pybind11>=2.7.0"],
    install_requires=["pybind11>=2.7.0"],
    # Currently, build_ext only provides an optional "highest supported C++
    # level" feature, but in the future it may provide more features.
    cmdclass={"build_ext": build_ext},  # type: ignore
    zip_safe=False,
)
