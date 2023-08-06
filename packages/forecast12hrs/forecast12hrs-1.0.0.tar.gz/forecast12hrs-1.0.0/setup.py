from setuptools import setup
setup(
    name='forecast12hrs',
    packages=['forecast12hrs'],
    version='1.0.0',
    license='MIT',
    description='Weather forecast data',
    author='Ray',
    install_requires = [
        'requests'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        
    ]

)