# TitleScraper

TitleScraper is a simple program to catch \[parts of\] a title of an open window, and outputs it to a file on your desktop.

![](https://voxelfox.co.uk/static/images/titlescraper/main.png)

## Use Cases

This system is useful for those who stream with Spotify or another program playing music, and want its song title output onto your stream. By selecting the file you're outputting to as a source in your OBS settings, you can have a constantly updating song tracker on your screen.

## Usage

**Window match regex** is the string/regex to search for in each open window's executable name. For example, the regex `firefox` would match any `firefox.exe` window.

**Title match regex** is the string/regex to search for in each of the matching window's titles. If you used the regex `(.+) - (.+)`, then any titles from `firefox.exe` windows with a hyphen and two spaces in them would be matched.

**File output regex** is the ouptut string to be put into the given file. If your output regex was `\1` then the first group before the hyphen would be matched.

**File output location** is the location where the file output is written.
