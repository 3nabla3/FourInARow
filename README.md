# Unbeatable? Four in a Row

## How to run?
Create a virtual env

```shell
python3 -m venv venv
. venv/bin/activate
```

Make sure all dependencies are installed

```shell
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

Run the program

```shell
python3 gui.py
```

## How to play?
To select a column, click on the column with the mouse, or use the numbers on
the keyboard.

To reset the board, press 'r'

Tip: keep the terminal open, it shows some information about what the 
algorithm is doing


## Settings
There are multiple variables at the top of gui.py to change some simple settings

## How to run tests?
```shell
python3 -m pytest -n $(nproc) -v
```

(make sure you have the virtual env and all the requirements installed)
