This Python script can be used to scrape https://www.instagram.com/explore/tags/HASHTAG page and for every post it stores:

1) Content of the picture
2) Related Hashtags

It is a very interesting tool to discover trending hashtags and relative content. Data are first stored into a csv file and then plotted using matplotlib.

The python script uses the *selenium* library to interact with the Selenium WebDriver which is used to automate browser operations. In order to install:

`pip install selenium`

Selenium requires a driver to interface with the chosen browser. In my case I used Chrome. Chrome driver can be downloaded from https://sites.google.com/a/chromium.org/chromedriver/downloads.
The path to this file has to be added to the PATH system variable, in order for Python to be able to locate it while executing. For more information in how installing and setup Selenium WebDriver visit https://pypi.org/project/selenium/.







