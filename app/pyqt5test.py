import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from keylogging import startlogging

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        # set title
        self.setWindowTitle("Hello World!")

        # set vertical layout
        self.setLayout(qtw.QVBoxLayout())

        # create a label
        my_label = qtw.QLabel("click to start logging")
        # change font size
        my_label.setFont(qtg.QFont('Helvetica', 18))
        self.layout().addWidget(my_label)

        # create a button
        my_button = qtw.QPushButton("Press Me!", clicked = lambda: press_it())
        self.layout().addWidget(my_button)

        self.show()

        def press_it():
            string = ''
            print(string)
            keys = startlogging()
            for key in keys:
                if key.split(' ')[1] != 'release':
                    print(key)
                    string += key.split(' ')[0].replace("'", "")

            print(string)

            my_label.setText(f'your message is: {string}')

app = qtw.QApplication([])
mw = MainWindow()

# run app
app.exec_()