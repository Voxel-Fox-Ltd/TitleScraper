from __future__ import annotations

import sys
import os
import json
import logging

from PyQt6.QtWidgets import QApplication, QGridLayout, QLabel, QWidget, QLineEdit

from _types import TitleScraperSettings
from _threads import TitleScraperThread


app = QApplication(sys.argv)
SETTINGS_FILE_LOCATION = os.path.join(os.getenv("APPDATA", r"%appdata%"), "TitleScraper", "config")
SETTINGS_FILE_DIR = os.path.join(os.getenv("APPDATA", r"%appdata%"), "TitleScraper")


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
_log = logging.getLogger("titlescraper")


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        # Set title - it WILL be changed but that's fine
        self.setWindowTitle("TitleScraper")

        # Make grid layout
        grid = QGridLayout()
        grid.setSpacing(5)

        # Make our labels
        title_match_regex_label = QLabel("Title Match Regex")
        window_match_regex_label = QLabel("Window Match Regex")
        file_output_regex_label = QLabel("File Output Regex")
        file_output_location_label = QLabel("File Output Location")

        # Make our inputs
        self.title_match_regex = title_match_regex = QLineEdit()
        self.window_match_regex = window_match_regex = QLineEdit()
        self.file_output_regex = file_output_regex = QLineEdit()
        self.file_output_location = file_output_location = QLineEdit()

        # Load up the settings file
        self.settings: TitleScraperSettings = None
        self.settings = self.load_settings()

        # Set default content for the inputs
        title_match_regex.setText(self.settings['title_match_regex'])
        window_match_regex.setText(self.settings['window_match_regex'])
        file_output_regex.setText(self.settings['file_output_regex'])
        file_output_location.setText(self.settings['file_output_location'])

        # Set actions for each input
        title_match_regex.textEdited.connect(self.save_settings)
        window_match_regex.textEdited.connect(self.save_settings)
        file_output_regex.textEdited.connect(self.save_settings)
        file_output_location.textEdited.connect(self.save_settings)

        # Add the widgets to the grid
        grid.addWidget(window_match_regex_label, 0, 0)
        grid.addWidget(title_match_regex_label, 1, 0)
        grid.addWidget(file_output_regex_label, 2, 0)
        grid.addWidget(file_output_location_label, 3, 0)
        grid.addWidget(window_match_regex, 0, 1)
        grid.addWidget(title_match_regex, 1, 1)
        grid.addWidget(file_output_regex, 2, 1)
        grid.addWidget(file_output_location, 3, 1)

        # Set layout and size
        self.setLayout(grid)
        self.setFixedSize(600, 150)

        # Run our stuff in threads
        self.mainloop = TitleScraperThread(self)
        self.mainloop.title_match_regex = title_match_regex
        self.mainloop.window_match_regex = window_match_regex
        self.mainloop.file_output_regex = file_output_regex
        self.mainloop.start()

    def save_settings(self) -> None:
        """
        Save the settings of the script.
        """

        self.settings = {
            "title_match_regex": self.title_match_regex.text(),
            "window_match_regex": self.window_match_regex.text(),
            "file_output_regex": self.file_output_regex.text(),
            "file_output_location": self.file_output_location.text(),
        }
        os.makedirs(SETTINGS_FILE_DIR, exist_ok=True)
        with open(SETTINGS_FILE_LOCATION, "w") as a:
            json.dump(self.settings, a)
        _log.info(f"Saved settings ({self.settings!r})")

    def load_settings(self) -> TitleScraperSettings:
        """
        Load the settings of the script from file.
        """

        data: TitleScraperSettings
        try:
            with open(SETTINGS_FILE_LOCATION) as a:
                data = json.load(a)
        except FileNotFoundError:
            data = {
                "title_match_regex": r"(?:\(\d+\) )?(.+?) - YouTube — (.+)",
                "window_match_regex": "",
                "file_output_regex": r"\1",
                "file_output_location": "title.txt",
            }
            self.save_settings()
        return data

    def save_content(self, content: str):
        """
        Save the content to the file location.
        """

        try:
            with open(self.file_output_location.text(), "w", encoding="utf-8") as a:
                a.write(content)
        except Exception as e:
            _log.error("err", exc_info=e)
        # _log.info(f"Saved content ({content!r}) to location ({self.file_output_location.text()})")


window = MainWindow()
window.show()
app.exec()
