# Maggie
Maggie is an collection of autotests for [Portus](http://port.us.org/). Currently it's in the POC stage. 

Portus is an authorization service and frontend for Docker registry (v2).

This project was written in Python and it uses [Splinter library](https://splinter.readthedocs.io/en/latest/)

##Preparations

1) First of all you'll need a couple of additional libraries. Each of them can be installed via **pip** https://pypi.python.org/pypi/pip

```
$ pip install selenium splinter
```
It’s important to note that you also need to have Google Chrome installed on your machine.

2) Then you need to clone current repository 
``` 
$ git clone https://github.com/Evalle/maggie.git
```

3) Now you can run **maggie** (see Examples section).


### Free software

- Copyright (C) 2016 Evgeny Shmarnev shmarnev@gmail.com

Maggie - is a free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Maggie is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
