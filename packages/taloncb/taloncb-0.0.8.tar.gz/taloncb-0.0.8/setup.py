from __future__ import absolute_import
from setuptools import setup, find_packages
import codecs
import os
from setuptools import setup, find_packages
from setuptools.command.install import install

class InstallCommand(install):
    user_options = install.user_options + [
        ('no-ml', None, "Don't install without Machine Learning modules."),
    ]

    boolean_options = install.boolean_options + ['no-ml']

    def initialize_options(self):
        install.initialize_options(self)
        self.no_ml = None

    def finalize_options(self):
        install.finalize_options(self)
        if self.no_ml:
            dist = self.distribution
            dist.packages=find_packages(exclude=[
                "tests",
                "tests.*",
                "taloncb.signature",
                "taloncb.signature.*",
            ])
            for not_required in ["numpy", "scipy", "scikit-learn==0.24.1"]:
                dist.install_requires.remove(not_required)

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.8'
DESCRIPTION = 'email signature extraction'
LONG_DESCRIPTION = 'returns the signature and body of an email'

# Setting up
setup(
    name="taloncb",
    version="0.0.8",
    author="camillebrl (Camille Barboule)",
    author_email="camille.barboule@gmail.com",
    description="signature extraction",
    long_description_content_type="text/markdown",
    cmdclass={
          'install': InstallCommand,
      },
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    zip_safe=True, 
    install_requires=[
          "lxml>=2.3.3",
          "regex>=1",
          "numpy",
          "scipy",
          "scikit-learn==0.24.1", # pickled versions of classifier, else rebuild
          "chardet>=1.0.1",
          "cchardet>=0.3.5",
          "cssselect",
          "six>=1.10.0",
          "html5lib",
          "joblib",
          ],
    tests_require=[
          "mock",
          "nose>=1.2.1",
          "coverage"
          ],
    keywords=['python', 'email', 'signature'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
