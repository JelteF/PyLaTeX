# set up

```sh
$sudo apt-get install texlive-pictures texlive-science texlive-latex-extra latexmk texlive-xetex
```

# install fonts

```sh
$tar -zxvf THSarabun.tar.gz --one-top-level
$cp ./THSarabun/*.ttf ~/.local/share/fonts/
$fc-cache -fv
```

# build latex

```python
python basic.py
```