from PySide6 import QtWidgets

from ui.easteregg import Ui_Form


class EasterEgg(QtWidgets.QWidget):
    def __init__(self, detail=False):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)

        if not detail:
            self.ui.label.setText(
                self.tr(
                    "Author: Guo Xianghao, male, born in April 1970, graduated from Beijing University of Posts and Telecommunications in 1998 with a Ph.D. in artificial intelligence and natural language processing. Currently engaged in natural language processing research and software development. Loves games so much that he develops his own. Lived in Beijing for more than 10 years."
                )
            )
        else:
            self.ui.label.setText(
                self.tr(
                    "I love nature, art, and literature. I mainly use C/C++ for programming, but I am also very familiar with 80x86 assembly language. I once wrote a computer virus for my girlfriend (now the mother of my child). I am also proficient in LISP and Prolog languages, and have in-depth research on information retrieval technology and concept retrieval technology."
                )
            )
