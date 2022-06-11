#!/usr/bin/env python3
# 2021 nr@bulme.at

from gpiozero import Button
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QLCDNumber,
    QVBoxLayout, QApplication)

DOWN_PIN = 22
RESET_PIN = 27
UP_PIN = 17 

class QtButton(QObject):
    changed = pyqtSignal()

    def __init__(self, pin):
        super().__init__()
        self.button = Button(pin) 
        self.button.when_pressed = self.gpioChange        

    def gpioChange(self):
        self.changed.emit()

class Counter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.count = 0

    def initUi(self):
        self.lcd = QLCDNumber()
        self.lcd.display(0)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lcd)

        self.setLayout(vbox)
        self.setMinimumSize(400, 200)
        self.setWindowTitle('Counter')
        self.show()


    def countUp(self):
        if self.count == 15:
            self.count = 0
            self.lcd.display(self.count)
        else:
            self.count += 1
            self.lcd.display(self.count)
    
    def countDown(self):
        if self.count == 0:
            self.count = 15
            self.lcd.display(self.count)
        else:
            self.count -= 1
            self.lcd.display(self.count)
        
    def countReset(self):
        self.count = 0
        self.lcd.display(self.count)
 

if __name__ ==  '__main__':
    app = QApplication([])
    gui = Counter()
    buttonUp = QtButton(UP_PIN)
    buttonUp.changed.connect(gui.countUp)
    buttonDown = QtButton(DOWN_PIN)
    buttonDown.changed.connect(gui.countDown)
    buttonReset = QtButton(RESET_PIN)
    buttonReset.changed.connect(gui.countReset)
    app.exec_()
    
