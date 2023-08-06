Usage by example
================

+----------------------------------------------------+-------------------------------------------------------------------+
| Command                                            | Result                                                            |
+----------------------------------------------------+-------------------------------------------------------------------+
| `mingw-to-msys clone -o D:\w\tmp`                  | clones MINGW-packages.git to `D:\w\tmp\MINGW-packages`            |
|                                                    | and MSYS2-packages.git to `D:\w\tmp\MSYS2-packages`               |
|                                                    | and stores paths in `%APPDATA%\mingw-to-msys\config.json`         |
+----------------------------------------------------+-------------------------------------------------------------------+
| `mingw-to-msys deps -p python-setuptools`          | prints dependencies of package `python-setuptools`                |
|                                                    | parsed from `MINGW-packages\mingw-w64-python-setuptools\PKGBUILD` |
+----------------------------------------------------+-------------------------------------------------------------------+
| `mingw-to-msys graph -p python-cryptography`       | prints dependency graph in dot language (for graphviz)            |
+----------------------------------------------------+-------------------------------------------------------------------+
| `mingw-to-msys convert -p python-idna -o D:\w\tmp` | converts `MINGW-packages\mingw-w64-python-idna`                   |
|                                                    | to `D:\w\tmp\python-idna`,                                        |
|                                                    | replacing mingw-specific variables in `PKGBUILD`                  |
+----------------------------------------------------+-------------------------------------------------------------------+