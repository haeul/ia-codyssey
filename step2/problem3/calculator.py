import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('iPhone Calculator')
        self.setFixedSize(360, 600)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        self.setStyleSheet('background-color: black;')

        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet('font-size: 50px; height: 100px; background: black; color: white; border: none;')
        main_layout.addWidget(self.display)

        button_layout = QGridLayout()
        button_layout.setSpacing(10)

        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        for row, line in enumerate(buttons):
            for col, text in enumerate(line):
                button = QPushButton(text)
                button.setFixedHeight(80)
                
                if text == '0':
                    button.setFixedWidth(160)
                    button.setStyleSheet(self.get_button_style(text) + 'text-align: left; padding-left: 30px;')
                else:
                    button.setFixedWidth(80)
                    button.setStyleSheet(self.get_button_style(text))

                button.clicked.connect(self.button_clicked)

                if text == '0':
                    button_layout.addWidget(button, row + 1, 0, 1, 2)
                else:
                    adjusted_col = col if row != 4 else col + 1
                    button_layout.addWidget(button, row + 1, adjusted_col)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.current_input = ''

    def get_button_style(self, text):
        '''버튼 색깔 스타일'''
        base = 'border-radius: 40px; font-size: 32px; font-weight: bold;'
        if text in ['AC', '+/-', '%']:
            return base + 'background-color: #a5a5a5; color: black;'
        elif text in ['÷', '×', '-', '+', '=']:
            return base + 'background-color: #ff9500; color: white;'
        else:
            return base + 'background-color: #333333; color: white;'

    def button_clicked(self):
        button = self.sender()
        text = button.text()

        if text == 'AC':
            self.current_input = ''
        elif text == '=':
            try:
                expression = self.current_input.replace('×', '*').replace('÷', '/')
                result = eval(expression)
                self.current_input = str(result)
            except Exception:
                self.current_input = 'Error'
        else:
            if self.current_input == '0' and text not in ['.', '+', '-', '×', '÷']:
                self.current_input = text
            else:
                self.current_input += text

        self.display.setText(self.current_input)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
