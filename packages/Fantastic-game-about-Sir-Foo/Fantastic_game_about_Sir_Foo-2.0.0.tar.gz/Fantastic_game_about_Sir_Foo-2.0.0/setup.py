from distutils.core import setup

with open('README') as file:
    readme = file.read()

setup(
    name='Fantastic_game_about_Sir_Foo',
    version='2.0.0',
    packages=['wargame'],
    url='https://test.pypi.org/pypi/Fantastic_game_about_Sir_Foo',
    license='LICENSE.txt',
    description='My Fantasy Game',
    long_description=readme,
    author='Karanaev K.A.',
    author_email='karanaevkosnya@gmail.com'
)