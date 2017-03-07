from setuptools import setup

setup(
    name='ticketer',
    packages=['ticketer'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-mysql',
        'pytest'
    ],
)
