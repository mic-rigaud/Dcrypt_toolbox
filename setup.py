from setuptools import setup

setup(
    name='Dcrypt_toolbox_v0.1',
    version='0.1',
    packages=['Dcrypt_toolbox', 'Dcrypt_toolbox.plugins'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        Dcrypt=Dcrypt_toolbox.main:main
    ''',
)
