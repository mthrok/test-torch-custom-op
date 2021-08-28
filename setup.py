#!/usr/bin/env python
import distutils.sysconfig
import os
from pathlib import Path
from setuptools import (
    setup,
    find_packages,
    Extension,
)
from setuptools.command.build_ext import build_ext
import subprocess

import torch

_THIS_DIR = Path(__file__).parent.resolve()


class CMakeBuild(build_ext):
    def run(self):
        try:
            subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake is not available.")
        super().run()

    def build_extension(self, ext):
        extdir = os.path.abspath(
            os.path.dirname(self.get_ext_fullpath(ext.name)))

        # required for auto-detection of auxiliary "native" libs
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        cfg = "Debug" if self.debug else "Release"

        cmake_args = [
            "-GNinja",
            f"-DCMAKE_BUILD_TYPE={cfg}",
            f"-DCMAKE_PREFIX_PATH={torch.utils.cmake_prefix_path}",
            f"-DCMAKE_INSTALL_PREFIX={extdir}",
            '-DCMAKE_VERBOSE_MAKEFILE=ON',
            f"-DPython_INCLUDE_DIR={distutils.sysconfig.get_python_inc()}",
        ]
        build_args = [
            '--target', 'install'
        ]
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        subprocess.check_call(
            ["cmake", str(_THIS_DIR)] + cmake_args, cwd=self.build_temp)
        subprocess.check_call(
            ["cmake", "--build", "."] + build_args, cwd=self.build_temp)

    def get_ext_filename(self, fullname):
        ext_filename = super().get_ext_filename(fullname)
        ext_filename_parts = ext_filename.split('.')
        without_abi = ext_filename_parts[:-2] + ext_filename_parts[-1:]
        ext_filename = '.'.join(without_abi)
        return ext_filename


def _main():
    setup(
        name="foo",
        version="0.1.0",
        description=(
            "Demonstration of loading custom ops from dynamic library "
            "which is not given to torch.ops.load_library"
        ),
        packages=find_packages(exclude=["src"]),
        ext_modules=[
            Extension(name='foo._foo', sources=[]),
            Extension(name='foo.libfoo', sources=[]),
        ],
        cmdclass={
            'build_ext': CMakeBuild,
        },
        install_requires=[
            'torch >= 1.7',
        ],
        zip_safe=False,
    )


if __name__ == '__main__':
    _main()
