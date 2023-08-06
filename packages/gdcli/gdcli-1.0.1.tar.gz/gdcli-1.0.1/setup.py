from setuptools import setup, find_packages
setup(
    name="gdcli",
    version="1.0.1",
    author="Subrahmanya s hegade",
    description="Command line too used for simple google dorks",
    packages=find_packages(include=['gdcli', 'gdcli.*']),
    entry_points='''
    [console_scripts]
    gdcli=gdcli.gd:start
    '''

)
