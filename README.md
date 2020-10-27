# rmout

'rmout' is a tool for throwing unnecessary files in a directory into the trash.
Create a list of file extensions to be deleted in the home directory and current directory in advance with the name ".rmoutrc".


## Installation


Anaconda, venv

```sh
$ pip install rmout
```


## Usage

simple.

```sh
$ rmout
```

In "send to trash [a]:", enter the extension code of the file you want to send to the Trash.
If you press the ENTER key without typing, the files with the extensions listed will be sent from the directory to the Trash.


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
send to trash [a]: 1
job01.com
job02.com
finished.
```
