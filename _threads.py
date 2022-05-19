import re
import logging
from PyQt6.QtWidgets import QLineEdit

import win32gui
import win32process
import psutil
from PyQt6.QtCore import QThread


_log = logging.getLogger("titlescraper._threads")


class TitleScraperThread(QThread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title_match_regex: QLineEdit
        self.window_match_regex: QLineEdit
        self.file_output_regex: QLineEdit


    def get_window_executable(self, thread_id: int) -> str:
        """
        Get the name of the executable from a thread ID.
        """

        process_ids = win32process.GetWindowThreadProcessId(thread_id)
        return psutil.Process(process_ids[-1]).name()

    def _enum_windows_callback(self, thread_id: int, _):
        """
        Save the title.
        """

        # See if the item is a window
        if not win32gui.IsWindow(thread_id):
            return True

        # Get the title and window name
        title = win32gui.GetWindowText(thread_id)
        if not title.strip():
            return True
        window = self.get_window_executable(thread_id)
        # _log.info(f"{window}")

        # See if it matches the title regex
        if re.search(self.title_match_regex.text(), title, re.IGNORECASE):

            # See if it matches the window regex
            if self.window_match_regex.text():
                match = re.search(self.window_match_regex.text(), window, re.IGNORECASE)
                if match:

                    # Output to file
                    output = title
                    output = re.sub(
                        self.title_match_regex.text(),
                        self.file_output_regex.text(),
                        title,
                    )
                    self.parent().save_content(output)  # type: ignore

                    # Return false so the enum stops
                    return False

        # Return true so we continue enumerating
        return True

    def run(self):
        """
        The main loop for the window handler.
        """

        while True:
            try:
                win32gui.EnumWindows(self._enum_windows_callback, 0)
            except Exception as e:
                # _log.error("err", exc_info=e)
                pass
            self.msleep(100)
