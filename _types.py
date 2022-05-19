from typing import TypedDict


class TitleScraperSettings(TypedDict):
    title_match_regex: str
    window_match_regex: str
    file_output_regex: str
    file_output_location: str
