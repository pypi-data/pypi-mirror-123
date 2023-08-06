from distutils.core import setup

with open('README') as file:
    readme = file.read()

setup(
    name             = 'Play_with_Sir_Foo',
    version          = '2.0.0',
    packages         = ['wargame'],
    url              = 'https://test.pypi.org/pypi/Play_with_Sir_Foo',
    license          = 'LICENSE.txt',
    description      = 'My Fantasy Game',
    long_description = readme,
    author           = 'Etrukova Dasha',
    author_email     = 'etrukovadasha@mail.ru'
)