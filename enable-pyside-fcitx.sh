#!/usr/bin/env bash
# use this script to enable fcitx for pyside6-designer/linguist
cp /usr/lib/qt6/plugins/platforminputcontexts/libfcitx5platforminputcontextplugin.so venv/lib/python3.12/site-packages/PySide6/Qt/plugins/platforminputcontexts/
