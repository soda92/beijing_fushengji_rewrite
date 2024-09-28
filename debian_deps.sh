sudo apt install libxcb-cursor0 libxcb-icccm4 libxcb-keysyms1
# find missing dependencies:
ldd venv/lib/python3.11/site-packages/PySide6/Qt/plugins/platforms/libqxcb.so | grep -i "not found"
# for error:
```
qt.qpa.plugin: From 6.5.0, xcb-cursor0 or libxcb-cursor0 is needed to load the Qt xcb platform plugin.
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: vkkhrdisplay, linuxfb, offscreen, minimalegl, eglfs, minimal, wayland, wayland-egl, xcb, vnc.

Aborted
```
references:
https://stackoverflow.com/q/68036484/12291425
