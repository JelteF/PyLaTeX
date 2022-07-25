# demo pylatex for thai

## set up dependencies

```sh
$sudo apt-get install texlive-pictures texlive-science texlive-latex-extra latexmk texlive-xetex
```

## install fonts

```sh
$export TEMP_PATH="/tmp/pylatex"
$mkdir -p $TEMP_PATH 
$curl -L https://github.com/wasit7/PyLaTeX/raw/master/examples/thai/THSarabun.tar.gz | tar -xz -C $TEMP_PATH
$cp $TEMP_PATH/*.ttf ~/.local/share/fonts/
$fc-cache -fv
```

## build latex

```python
python basic.py
```