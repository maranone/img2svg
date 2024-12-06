from setuptools import setup, find_packages

setup(
    name='img2svg',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'Pillow',
        'opencv-python',
        'svgwrite',
        'numpy'
    ],
    entry_points={
        'console_scripts': [
            'img2svg=img2svg.cli:main',
        ],
    },
)
