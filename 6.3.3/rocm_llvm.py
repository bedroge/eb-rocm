# -*- coding: utf-8 -*-
##
# Copyright 2009-2025 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://www.vscentrum.be),
# Flemish Research Foundation (FWO) (http://www.fwo.be/en)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# https://github.com/easybuilders/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
EasyBuild support for building and installing ROCm-LLVM, AMD's fork of the LLVM compiler infrastructure.

@author: Bob Dröge (University of Groningen)
"""
import glob
import os

from easybuild.tools import LooseVersion
from easybuild.easyblocks.clang import DEFAULT_TARGETS_MAP as LLVM_ARCH_MAP
from easybuild.easyblocks.llvm import EB_LLVM
from easybuild.easyblocks.generic.bundle import Bundle
from easybuild.framework.easyblock import EasyBlock
from easybuild.framework.easyconfig import CUSTOM
from easybuild.tools.build_log import EasyBuildError, print_msg, print_warning
from easybuild.tools.modules import get_software_root
from easybuild.tools.systemtools import AARCH64, POWER, X86_64, get_cpu_architecture, get_shared_lib_ext


# Default AMD GPU architectures to build for
#
# AMD uses 'gfx' to identify the GPU, the first number identifies the generation, according to
# https://www.x.org/wiki/RadeonFeature/#index5h2 while the rest identifies the specific GPU.
# In the context of EasyBuild this identifier can be thought of as equivalent to the 'sm_<xx>'
# nomenclature of Nvidia.
#DEFAULT_GFX_ARCHS = ['gfx900', 'gfx902', 'gfx906', 'gfx908', 'gfx90a', 'gfx1030', 'gfx1031']
DEFAULT_GFX_ARCHS = [
    'gfx700', 'gfx701',
    'gfx801', 'gfx803',
    'gfx900', 'gfx902', 'gfx906', 'gfx908', 'gfx90a', 'gfx90c', 'gfx940',
    'gfx1010', 'gfx1030', 'gfx1031', 'gfx1032', 'gfx1033', 'gfx1034', 'gfx1035', 'gfx1036',
    'gfx1100', 'gfx1101', 'gfx1102', 'gfx1103',
]


class EB_ROCm_minus_LLVM(EB_LLVM):
    """
    Self-contained build of AOMP version of Clang
    """

    def __init__(self, *args, **kwargs):
        """Initialize LLVM-specific variables."""
        super(EB_ROCm_minus_LLVM, self).__init__(*args, **kwargs)
        self.final_projects.remove('flang')
        self.final_projects.remove('mlir')
        #self.final_projects.remove('openmp')
        #self.final_runtimes.append('openmp')

#    def configure_step3(self):
#      super(EB_ROCm_minus_LLVM, self).configure_step3()
#      return
#      print_msg("device libs")
#      device_libs_src_dir = os.path.join(self.llvm_src_dir, 'amd', 'device-libs')
#      device_libs_build_dir = os.path.join(self.llvm_src_dir, '..', 'devicelibs.obj')
#      self._configure_general_build()
#      self._cmakeopts = {'LLVM_DIR': os.path.join(self.llvm_obj_dir_stage2, 'lib', 'cmake', 'llvm')}
#      self.add_cmake_opts()
#      super(EB_LLVM, self).configure_step(builddir=device_libs_build_dir, srcdir=device_libs_src_dir)
#      super(EB_LLVM, self).build_step()
#      super(EB_LLVM, self).install_step()

#      super(EB_ROCm_minus_LLVM, self).configure_step3()
      #self._cmakeopts.update({'LIBOMP_OMP_TOOLS_INCLUDE_DIR': os.path.join(self.llvm_obj_dir_stage3, 'projects', 'openmp', 'runtime', 'src')})
      #self._cmakeopts.update({'LIBOMPTARGET_NVPTX_COMPUTE_CAPABILITIES': '"60;61;62;70;72;75;80;86;89;90"'})
      # add openmp flags
