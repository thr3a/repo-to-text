```
usage: repo-to-text.py [-h] [-d DIRECTORIES [DIRECTORIES ...]] [-f FILES [FILES ...]] [-i IGNORE_DIRS [IGNORE_DIRS ...]]
                       [-e EXTENSIONS [EXTENSIONS ...]]

options:
  -h, --help            show this help message and exit
  -d DIRECTORIES [DIRECTORIES ...], --directories DIRECTORIES [DIRECTORIES ...]
                        検索対象のディレクトリパス (複数指定可能)
  -f FILES [FILES ...], --files FILES [FILES ...]
                        検索対象のファイルパス (複数指定可能)
  -i IGNORE_DIRS [IGNORE_DIRS ...], --ignore-dirs IGNORE_DIRS [IGNORE_DIRS ...]
                        除外するディレクトリ名 (複数指定可能)
  -e EXTENSIONS [EXTENSIONS ...], --extensions EXTENSIONS [EXTENSIONS ...]
                        検索対象の拡張子 (複数指定可能)
```

例

```sh
python repo-to-text.py -d ./src -f package.json -e .ts .tsx > result.md
```
