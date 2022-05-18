import sys

from PyQt6.QtWidgets import QApplication, QGridLayout, QLabel, QWidget, QLineEdit


app = QApplication(sys.argv)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("TitleScraper")

        grid = QGridLayout()
        grid.setSpacing(10)

        title_match_regex_label = QLabel("Title Match Regex")
        window_match_regex_label = QLabel("Window Match Regex")
        file_output_regex_label = QLabel("File Output Regex")
        file_output_location_label = QLabel("File Output Location")

        self.title_match_regex = title_match_regex = QLineEdit()
        self.window_match_regex = window_match_regex = QLineEdit()
        self.file_output_regex = file_output_regex = QLineEdit()
        self.file_output_location = file_output_location = QLineEdit()

        self.file_output_location.textChanged.connect(lambda t: print(t))

        grid.addWidget(title_match_regex_label, 0, 0)
        grid.addWidget(window_match_regex_label, 1, 0)
        grid.addWidget(file_output_regex_label, 2, 0)
        grid.addWidget(file_output_location_label, 3, 0)
        grid.addWidget(title_match_regex, 0, 1)
        grid.addWidget(window_match_regex, 1, 1)
        grid.addWidget(file_output_regex, 2, 1)
        grid.addWidget(file_output_location, 3, 1)

        self.setLayout(grid)
        self.setFixedSize(600, 150)


window = MainWindow()
window.show()
app.exec()
