import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()         # UI 구성 초기화
        self.reset()           # 계산기 상태 초기화

    def init_ui(self):
        self.setWindowTitle('iPhone Calculator')   # 창 제목 설정
        self.setFixedSize(360, 600)                # 고정된 창 크기

        main_layout = QVBoxLayout()                # 전체 수직 레이아웃
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        self.setStyleSheet('background-color: black;')  # 배경색 검정

        # 결과 출력 디스플레이 구성
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)                 # 직접 입력 막기
        self.display.setAlignment(Qt.AlignRight)       # 오른쪽 정렬
        self.display.setStyleSheet('font-size: 50px; height: 100px; background: black; color: white; border: none;')
        main_layout.addWidget(self.display)

        button_layout = QGridLayout()                  # 버튼 레이아웃 (그리드)
        button_layout.setSpacing(10)

        # 버튼 배치 (아이폰 계산기 구조)
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

                # 0은 넓은 버튼
                button.setFixedWidth(160 if text == '0' else 80)
                style = self.get_button_style(text)

                # 왼쪽 정렬 스타일 (0번만)
                if text == '0':
                    style += 'text-align: left; padding-left: 30px;'
                    button_layout.addWidget(button, row + 1, 0, 1, 2)  # 0은 두 칸 차지
                else:
                    adjusted_col = col if row != 4 else col + 1       # 0이 두 칸 차지했으므로 위치 보정
                    button_layout.addWidget(button, row + 1, adjusted_col)

                button.setStyleSheet(style)
                button.clicked.connect(self.button_clicked)           # 버튼 클릭 이벤트 연결

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def get_button_style(self, text):
        '''버튼에 맞는 색상 및 폰트 설정'''
        base = 'border-radius: 40px; font-size: 32px; font-weight: bold;'
        if text in ['AC', '+/-', '%']:
            return base + 'background-color: #a5a5a5; color: black;'
        elif text in ['÷', '×', '-', '+', '=']:
            return base + 'background-color: #ff9500; color: white;'
        else:
            return base + 'background-color: #333333; color: white;'

    def reset(self):
        '''계산기 상태 초기화'''
        self.current_input = '0'
        self.pending_operator = ''
        self.last_number = None
        self.display.setText('0')

    def update_display(self):
        '''결과창에 값 출력, 길이에 따라 폰트 조정 및 반올림'''
        value = self.current_input
        if '.' in value and len(value.split('.')[-1]) > 6:
            value = str(round(float(value), 6))  # 소수점 6자리 이하로 반올림

        # 글자 길이에 따라 폰트 크기 조절
        if len(value) > 10:
            self.display.setStyleSheet('font-size: 30px; height: 100px; background: black; color: white; border: none;')
        else:
            self.display.setStyleSheet('font-size: 50px; height: 100px; background: black; color: white; border: none;')

        self.display.setText(value)

    def button_clicked(self):
        '''버튼 클릭 이벤트 처리'''
        text = self.sender().text()

        if text in '0123456789':
            self.append_digit(text)
        elif text == '.':
            self.append_dot()
        elif text in ['+', '-', '×', '÷']:
            self.set_operator(text)
        elif text == '=':
            self.equal()
        elif text == 'AC':
            self.reset()
        elif text == '+/-':
            self.negative_positive()
        elif text == '%':
            self.percent()

        self.update_display()

    def append_digit(self, digit):
        '''숫자 버튼 누를 때'''
        if self.current_input == '0':
            self.current_input = digit
        else:
            self.current_input += digit

    def append_dot(self):
        '''소수점 처리: 중복 방지'''
        if '.' not in self.current_input:
            self.current_input += '.'

    def set_operator(self, op):
        '''연산자 버튼 누를 때'''
        if self.current_input:
            if self.last_number is not None and self.pending_operator:
                self.equal()  # 이전 계산 먼저 실행
            self.last_number = float(self.current_input)
            self.pending_operator = op
            self.current_input = '0'

    def equal(self):
        '''= 버튼 처리: 계산 수행'''
        if self.pending_operator and self.last_number is not None:
            try:
                current = float(self.current_input)
                if self.pending_operator == '+':
                    result = self.last_number + current
                elif self.pending_operator == '-':
                    result = self.last_number - current
                elif self.pending_operator == '×':
                    result = self.last_number * current
                elif self.pending_operator == '÷':
                    if current == 0:
                        raise ZeroDivisionError
                    result = self.last_number / current
                self.current_input = str(result)
                self.last_number = None
                self.pending_operator = ''
            except ZeroDivisionError:
                self.current_input = 'Error'

    def negative_positive(self):
        '''+/- 버튼: 부호 반전'''
        if self.current_input.startswith('-'):
            self.current_input = self.current_input[1:]
        elif self.current_input != '0':
            self.current_input = '-' + self.current_input

    def percent(self):
        '''% 버튼: 백분율 변환'''
        try:
            self.current_input = str(float(self.current_input) / 100)
        except ValueError:
            self.current_input = 'Error'


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())  # 프로그램 종료 시까지 실행
