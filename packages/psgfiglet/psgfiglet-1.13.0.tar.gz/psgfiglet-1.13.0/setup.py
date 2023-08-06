import setuptools

setuptools.setup(
    name="psgfiglet",
    version="1.13.0",
    author="PySimpleGUI",
    author_email="PySimpleGUI@PySimpleGUI.org",
    description="Create Figlets using a PySimpleGUI GUI and pyfiglet",
    url="https://github.com/PySimpleGUI/psg-figlet",
    packages=['psgfiglet'],
    install_requires=['PySimpleGUI', 'pyfiglet'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Topic :: Multimedia :: Graphics",
        "Operating System :: OS Independent"
    ],
    entry_points={
        'gui_scripts': [
            'psgfiglet=psgfiglet.gui:main'
        ],
    },
)
