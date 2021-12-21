# rmout

rmout is a tool for throwing unnecessary files in a directory into the trash.


[![PyPI Version](https://img.shields.io/pypi/v/rmout.svg??style=flat)](https://pypi.org/project/rmout/)
![GitHub Actions](https://github.com/simulation-lab/rmout/workflows/GitHub%20Actions/badge.svg)
![CodeQL](https://github.com/simulation-lab/rmout/workflows/CodeQL/badge.svg)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)


## Installation


conda, venv

```sh
$ pip install rmout
```


## Usage

Create a ".rmoutrc" file under your home directory or current directory.
In the file, list the extensions of the files to be deleted.

example: `.rmoutrc` file

```.rmoutrc
.sim
.prt
.dat
```

Move to the directory containing the files you want to throw in the Trash and execute the following command.

```sh
$ rmout
```

In "send to trash [a] ? ", enter the extension code of the file you want to send to the Trash. The default is all files. If you press the ENTER key without typing, the files with the extensions listed will be sent from the directory to the Trash.

If you enter the code to the left of the extension list separated by commas, you can select the file with the extension you want to discard.



```sh
$ rmout
     1: *.com  2
     2: *.dat  2
     3: *.log  1
     4: *.msg  2
     5: *.odb  2
     6: *.oke  1
     7: *.prt  2
     8: *.sim  2
     9: *.sta  2
     a:  all files
     x:  exit
send to trash [a] ? 1, 5
job01.com
job02.com
job01.odb
job02.odb
finished.
```
