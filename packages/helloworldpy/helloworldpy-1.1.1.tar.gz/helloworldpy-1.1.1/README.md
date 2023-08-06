![PyPI - Python Version](https://img.shields.io/pypi/pyversions/helloworldpy)  ![PyPI - Status](https://img.shields.io/pypi/status/helloworldpy)  ![PyPI](https://img.shields.io/pypi/v/helloworldpy) ![PyPI - License](https://img.shields.io/pypi/l/helloworldpy)

# [helloworldpy]

## This is a basic project for learning how to make the PIP([PyPI]) package

### To install the package!

#### On Windows:

```bash 
$ pip install helloworldpy
```

#### On macOS and Linux:

```bash
$ sudo pip3 install helloworldpy
```

# Changelog

Check the [changelog here].

### Example:

```bash
$ helloworldpy -h                                                         
usage: helloworldpy [-h] [-V] [-n [NAME [NAME ...]]] [-ip] [-g]

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program version
  -n [NAME [NAME ...]], --name [NAME [NAME ...]]
                        output Hello Name! or Hello World!
  -ip, --checkip        This will check public IP address of system
  -g, --playgame        You can play Bulls and Cows game
```

# Usage

## helloworldpy --name (with out arguments)

```bash 
$ helloworldpy --name
  Hello World!
```

## helloworldpy --name (with arguments)

```bash 
$ helloworldpy --name py
  Hello Py!
```

## You Can Play [Bulls and Cows] Game

```bash 
$ helloworldpy --playgame

        ##############--->>> Rules: <<---################
        #   Note:                                       #
        #       Bulls = correct code, correct position. #
        #       Cows = correct code, wrong position.    #
        #################################################

how many digits number you need? 2
enter a number you guess: 12
Cow : 0,Bull : 0
enter a number you guess: 34
Cow : 0,Bull : 1
enter a number you guess: 56
Cow : 0,Bull : 0
enter a number you guess: 89
Cow : 0,Bull : 1
enter a number you guess: 94
Cow : 1,Bull : 0
enter a number you guess: 93
Cow : 2,Bull : 0
enter a number you guess: 39
Cow : 0,Bull : 2

                    |-------------------------------|
                                YOU WON!
                      * Answer is "39"
                      * Number of attempts are 7
                    |-------------------------------|


```

## Cheat codes were added

```bash

        ##############--->>> Rules: <<---################
        #   Note:                                       #
        #       Bulls = correct code, correct position. #
        #       Cows = correct code, wrong position.    #
        #################################################

how many digits number you need? 3
enter a number you guess: 124
Cow : 1,Bull : 0
enter a number you guess: 412
Cow : 1,Bull : 0
enter a number you guess: 421
Cow : 1,Bull : 0
enter a number you guess: 456
Cow : 0,Bull : 0
enter a number you guess: 132
Cow : 2,Bull : 0
enter a number you guess: 213
Cow : 0,Bull : 2
enter a number you guess: answer

        >>>>>
           Do you really want to give up?
                Don't Give Up!!
                I know you Can do it!
                                           <<<<<<

y/n : y

                    |---------------------------------------|
                                    YOU LOST!
                        * Answer is "203"
                        * Number of attempts are 7
                        * Because you used cheat code!!
                    |---------------------------------------|


```

## To Check System public IP Address

```bash 
$ helloworldpy --checkip
  Public IP Address: 130.242.022.330
```

- **Note:** The above IP is Demo

Build Guide:

```
python setup.py sdist bdist_wheel
twine check dist/*
```

# License

[MIT License]

Copyright (c) 2020 [Saketh Chandra]

[PyPI]: https://pypi.org/

[changelog here]: https://github.com/Saketh-Chandra/helloworldpy/releases/

[helloworldpy]: https://pypi.org/project/helloworldpy/

[Bulls and Cows]: https://en.wikipedia.org/wiki/Bulls_and_Cows#The_numerical_version

[MIT License]: https://github.com/Saketh-Chandra/helloworldpy/blob/master/LICENSE

[Saketh Chandra]: https://github.com/Saketh-Chandra/ 