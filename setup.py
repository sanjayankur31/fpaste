# We stick to distutils at the moment since it is part of the standard Python
# library.  Check with Python SIG if setuputils is expected in all Python
# installations or not
from distutils.core import setup
from fpaste.version import __version__

setup(
    name="fpaste",
    description="A pastebin cli util for fpaste.org",
    version=__version__,
    author="Jason 'zcat' Farrell and others at Fedora Unity",
    maintainer="Ankur Sinha",
    url="https://pagure.io/fpaste",
    license="GPLv3",
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
    ],
    scripts=['scripts/fpaste']
)
