# beijing fushengji rewrite

北京浮生记重制版

Rewrite [beijing fushengji][url] using Qt.

[url]: https://github.com/chrisguo/beijing_fushengji

Features:
 - all dialogs are reproduced.
 - support sounds.
 - Support Autosave.
 - Support both English and Simplified Chinese.


![main](https://github.com/soda92/beijing_fushengji_rewrite/raw/main/main.png)
![main_en](https://github.com/soda92/beijing_fushengji_rewrite/raw/main/main-en.png)

## Install package

`pip install beijing-fushengji`
`py -m beijing_fushengji`

## Run locally

1. Clone repo
1. install dependencies in `m-r.txt`
1. run `tools/compile_all.py`
1. Start app with `entry.py`

## Design Forms

Run `tools/design.py`

## Translation

Run `tools/translate.py`

## Other considerations

On debian, you need to install some dependencies first. see `debian_deps.sh`.

On linux with fcitx, need to copy some libs for `Linguist` to support Chinese. see `enable-pyside-fcitx.sh`.
