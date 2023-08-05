# Colab
Colab are the tools for curating colab gene test data to bgi-PETA.

## Installation
```
$ cd colab
$ python setup.py install
```

## Usage
```
$ colab -h
usage: colab [-h] -d ROOT_PATH [-s DATABASE] [-u]

tools for curating colab gene test data to bgi-PETA

optional arguments:
  -h, --help            show this help message and exit
  -d ROOT_PATH, --root_path ROOT_PATH
                        root path for the product files of a colab
  -s DATABASE, --database DATABASE
                        database login path
  -u, --update          update for existing samples, skip if False
```
