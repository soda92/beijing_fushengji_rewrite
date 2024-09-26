from PySide6 import QtWidgets
from ui.text_editor import Ui_TextEditor


class TextEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_TextEditor()
        self.ui.setupUi(self)
        self.move(
            QtWidgets.QApplication.screens()[0].geometry().center()
            - self.rect().center()
        )
        self.ui.check_grammar.setFocus()
        self.ui.check_grammar.clicked.connect(self.check_grammar)

    def check_grammar(self):
        QtWidgets.QMessageBox.information(self,
            self.tr("Grammar"), 
            self.tr('Spell check suggestion: "Fragrant air" changed to "Fresh air"; "Boss" changed to "Boss lady".'),
            QtWidgets.QMessageBox.StandardButton.Ok)

