
<p align="center">
  <img src="https://raw.githubusercontent.com/PySimpleGUI/PySimpleGUI/master/images/for_readme/Logo%20with%20text%20for%20GitHub%20Top.png" alt="Python GUIs for Humans">
  <h2 align="center">Figlet Creation</h2>
</p>

Create Figlets easily using this application created using PySimpleGUI.

## Installation

### Old-school Straight Pip

pip install psgfiglet

### pip via `python -m pip` the python recommended way

#### If `python` is your command

python -m pip install psgfiglet

#### If `python3` is your command

python3 -m pip install psgfiglet

## Usage

To run the program and create your own Figlets type from your command prompt:

psgfiglet




## About - What is a Figlet?

A Figlet is a text based way to add large block text to your code or chats.  There are a variety of "Fonts" available that you'll find listed along the left side of the screen.

![psgfiglet](https://user-images.githubusercontent.com/46163555/137602353-fe721a9b-271a-48b7-b121-8277f8035633.jpg)


## To use in your code

The easiest way to is make a multiline string in your code using triple quotes:

```python

'''
This is a multiline string
Line 2
'''
```


You can simply paste your Figlet into one of these multiline comments.  They work well at breaking up your code into chunks

```python

'''
                    oo          
                                
88d8b.d8b. .d8888b. dP 88d888b. 
88'`88'`88 88'  `88 88 88'  `88 
88  88  88 88.  .88 88 88    88 
dP  dP  dP `88888P8 dP dP    dP
'''

def main():
    x = 20

```


## Uses Open Source Packages

`pyfiglet` - "An implementation of figlet written in Python"

[https://github.com/pwaller/pyfiglet](https://github.com/pwaller/pyfiglet)
The pyfiglet package was generously licensed with an [MIT license](https://github.com/pwaller/pyfiglet/blob/master/LICENSE).


```
                  .8888b oo          dP            dP   
                  88   "             88            88   
88d888b. dP    dP 88aaa  dP .d8888b. 88 .d8888b. d8888P 
88'  `88 88    88 88     88 88'  `88 88 88ooood8   88   
88.  .88 88.  .88 88     88 88.  .88 88 88.  ...   88   
88Y888P' `8888P88 dP     dP `8888P88 dP `88888P'   dP   
88            .88                .88                    
dP        d8888P             d8888P
```


`PySimpleGUI`[www.PySimpleGUI.com](http://www.PySimpleGUI.com)



## Origin


```
                                             oo dP       
                                                88       
88d888b. dP    dP .d8888b. dP    dP 88d888b. dP 88  .dP  
88'  `88 88    88 88'  `"" 88    88 88'  `88 88 88888"   
88    88 88.  .88 88.  ... 88.  .88 88    88 88 88  `8b. 
dP    dP `8888P88 `88888P' `8888P88 dP    dP dP dP   `YP 
              .88               .88                      
          d8888P            d8888P
```

This program originated with user [nycynik](https://github.com/nycynik).with his [ascii-font-processor](https://github.com/nycynik/ascii-font-processor) project.

Then Mike from the PySimpleGUI project started with his project and modified it.

It's one of the many PySimpleGUI-based programs I use daily. It's the first in a series of "Application Releases" that are hosted on PyPI.org

## Special Thanks

```
                                                                           
                                                                           
 /__  ___/                                  \\    / /                      
   / /  / __      ___       __     / ___     \\  / /  ___                  
  / /  //   ) ) //   ) ) //   ) ) //\ \       \\/ / //   ) ) //   / /      
 / /  //   / / //   / / //   / / //  \ \       / / //   / / //   / /       
/ /  //   / / ((___( ( //   / / //    \ \     / / ((___/ / ((___( ( ()()()
```
Paolo Amoroso - showed us the path to successfully releasing PySimpleGUI applications via PyPI with his [Spacestills](https://pypi.org/project/spacestills/) project.

```
MM'""""'YMM dP                 a8888a           oo          M""""""""M 
M' .mmm. `M 88                d8' ..8b                      Mmmm  mmmM 
M  MMMMMooM 88d888b. 88d888b. 88 .P 88 88d888b. dP .d8888b. MMMM  MMMM 
M  MMMMMMMM 88'  `88 88'  `88 88 d' 88 88'  `88 88 88'  `"" MMMM  MMMM 
M. `MMM' .M 88    88 88       Y8'' .8P 88    88 88 88.  ... MMMM  MMMM 
MM.     .dM dP    dP dP        Y8888P  dP    dP dP `88888P' MMMM  MMMM 
MMMMMMMMMMM                                                 MMMMMMMMMM
```

[Tanay Findley](https://github.com/Chr0nicT) - Fantastic PySimpleGUI programmer that created a template to make  these console-less PySimpleGUI Applications.

## License

Licensed under an LGPL3 License

## This PyPI Was Designed and Written By

Mike from PySimpleGUI.org - The pieces assembler.

## Contributing

Like the PySimpleGUI project, this project is currently licensed under an open-source license, the project itself is structured like a proprietary product. Pull Requests are not accepted.

## Copyright

Copyright 2021 PySimpleGUI
