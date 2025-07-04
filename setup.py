# -*- coding: utf-8 -*-
# ######### COPYRIGHT #########
#
# Copyright(c) 2025
# -----------------
#
# * Université d'Aix Marseille (AMU) -
# * Centre National de la Recherche Scientifique (CNRS) -
# * Université de Toulon (UTLN).
# * Copyright © 2019-2025 AMU, CNRS, UTLN
#
# Contributors:
# ------------
#
# * Sokol Koço <sokol.koco_AT_lis-lab.fr>
# * Cécile Capponi <cecile.capponi_AT_univ-amu.fr>
# * Florent Jaillet <florent.jaillet_AT_math.cnrs.fr>
# * Dominique Benielli <dominique.benielli_AT_univ-amu.fr>
# * Riikka Huusari <rikka.huusari_AT_univ-amu.fr>
# * Baptiste Bauvin <baptiste.bauvin_AT_univ-amu.fr>
# * Hachem Kadri <hachem.kadri_AT_lis-lab.fr>
#
# Description:
# -----------
#
# The multimodal package implement classifiers multiview, 
# MumboClassifier class, MuComboClassifier class, MVML class, MKL class.
# compatible with sklearn
#
# Version:
# -------
#
# * multimodal version = 0.1.0
#
# Licence:
# -------
#
# License: New BSD License
#
# ######### COPYRIGHT #########
import os, re
import shutil
from setuptools import setup, find_packages
#from distutils.command.clean import clean as _clean
#from distutils.dir_util import remove_tree
#from distutils.command.sdist import sdist

from setuptools._distutils.dir_util import remove_tree
from setuptools.command.sdist import sdist
from setuptools import Command
try:
    import numpy
except:
    raise 'Cannot build iw without numpy'
    sys.exit()

# --------------------------------------------------------------------
# Clean target redefinition - force clean everything supprimer de la liste '^core\.*$',
relist = ['^.*~$', '^#.*#$', '^.*\.aux$', '^.*\.pyc$', '^.*\.o$']
reclean = []
USE_COPYRIGHT = True
try:
    from copyright import writeStamp, eraseStamp
except ImportError:
    USE_COPYRIGHT = False

###################
# Get Multimodal version
####################
def get_version():
    v_text = open('VERSION').read().strip()
    v_text_formted = '{"' + v_text.replace('\n', '","').replace(':', '":"')
    v_text_formted += '"}'
    v_dict = eval(v_text_formted)
    return v_dict["multimodal"]

########################
# Set Multimodal __version__
########################
def set_version(multimodal_dir, version):
    filename = os.path.join(multimodal_dir, '__init__.py')
    buf = ""
    for line in open(filename, "rb"):
        if not line.decode("utf8").startswith("__version__ ="):
            buf += line.decode("utf8")
    f = open(filename, "wb")
    f.write(buf.encode("utf8"))
    f.write(('__version__ = "%s"\n' % version).encode("utf8"))

for restring in relist:
    reclean.append(re.compile(restring))


def wselect(args, dirname, names):
    for n in names:
        for rev in reclean:
            if (rev.match(n)):
                os.remove("%s/%s" %(dirname, n))
        break


######################
# Custom clean command
######################
class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print("Running clean...")

        # Clean build folder
        if os.path.exists('build'):
            print("Removing build/")
            shutil.rmtree('build')

        # Clean egg-info
        if os.path.exists('scikit_multimodallearn.egg-info'):
            print("Removing egg-info/")
            shutil.rmtree('scikit_multimodallearn.egg-info')

        # Clean compiled files in multimodal/
        for dirpath, dirnames, filenames in os.walk('multimodal'):
            for filename in filenames:
                if filename.endswith(('.so', '.pyd', '.dll', '.pyc')):
                    file_path = os.path.join(dirpath, filename)
                    print(f"Removing file {file_path}")
                    os.remove(file_path)
            for dirname in dirnames:
                if dirname == '__pycache__':
                    cache_path = os.path.join(dirpath, dirname)
                    print(f"Removing {cache_path}")
                    shutil.rmtree(cache_path)

        print("Clean complete.")
# class clean(_clean):
#     def walkAndClean(self):
#         os.walk("..", wselect, [])
#         pass
#
#     def run(self):
#         clean.run(self)
#         if os.path.exists('build'):
#             shutil.rmtree('build')
#         for dirpath, dirnames, filenames in os.walk('multimodal'):
#             for filename in filenames:
#                 if (filename.endswith('.so') or
#                         filename.endswith('.pyd') or
#                         filename.endswith('.dll') or
#                         filename.endswith('.pyc')):
#                     os.unlink(os.path.join(dirpath, filename))
#             for dirname in dirnames:
#                 if dirname == '__pycache__':
#                     shutil.rmtree(os.path.join(dirpath, dirname))

##############################
# Custom sdist command
##############################
class m_sdist(sdist):
    """ Build source package

    WARNING : The stamping must be done on an default utf8 machine !
    """
    def run(self):
        if USE_COPYRIGHT:
            writeStamp()
            sdist.run(self)
            # eraseStamp()
        else:
            sdist.run(self)

def setup_package():
    """Setup function"""
    name  = 'scikit-multimodallearn'
    version = get_version()
    multimodal_dir = 'multimodal'
    set_version(multimodal_dir, version)
    here = os.path.abspath(os.path.dirname(__file__))
    long_description_content_type = 'text/x-rst'
    with open(os.path.join(here, 'README.rst'), encoding='utf-8') as readme:
        long_description = readme.read()
    group = 'dev'
    # url = 'https://gitlab.lis-lab.fr/{}/{}'.format(group, name)
    # project_urls = {
    #    'Documentation': 'http://{}.pages.lis-lab.fr/{}'.format(group, name),
    #    'Source': url,
    #   'Tracker': '{}/issues'.format(url)}
    packages = find_packages(exclude=['*.tests'])
    include_package_data = True
    extras_require = {
        'test': ["pytest", "pytest-cov"],
        'doc': ["sphinx==5.0", "numpydoc", "sphinx_gallery", "matplotlib", "sphinx_rtd_theme"]}
    # python_requires=python_requires, description=description,author=author,
    # classifiers=classifiers, keywords=keywords, install_requires=install_requires,
    setup(version=version,
          license="BSD-3-Clause",
          license_files="LICENSE",
          long_description=long_description,
          long_description_content_type=long_description_content_type,
          packages=packages,
          include_package_data=include_package_data,
          extras_require=extras_require)


if __name__ == "__main__":
    setup_package()
