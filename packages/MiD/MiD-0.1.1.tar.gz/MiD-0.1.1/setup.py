from setuptools import setup, find_packages
 
setup(
    name                = 'MiD',
    version             = '0.1.1',
    description         = 'Medical Deep Learning Framework',
    author              = 'seungyeob.seon',
    author_email        = 'liamseon@gmail.com',
    url                 = 'https://github.com/InGradient/InGradient_AI_Library',
    install_requires    =  ['SimpleITK'],
    packages            = find_packages(exclude = ['ingradient_library']),
    keywords            = ['pypi deploy'],
    package_data        = {},
    zip_safe            = False
)
