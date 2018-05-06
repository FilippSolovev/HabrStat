# HabrStat

Habr.com is the most popular technology blog in Russian, every day a number of articles appear there to be discussed by thousands of people.
HabrStat extracts three most frequent nouns that occur in titles of articles within a week.

# Example

To collect the statistics run the script with an argument specifying the number of web pages on Habrahabr.ru to scrape titles from like this:

~~~~
$ python habr_stat.py --pages=100

Beginning of the week End of the week        The most frequent words
          2018-04-30      2018-05-06            часть глава система
          2018-04-23      2018-04-29       часть система управление
          2018-04-16      2018-04-22  система приложение разработка
          2018-04-09      2018-04-15  часть приложение безопасность
          2018-04-02      2018-04-08    часть разработка приложение
~~~~

In case of omitting the argument script will gather titles from the first 10 pages.

# Installation

The project is written in Python3.
Clone the project and install the requirements:

~~~~
$ git clone https://github.com/FilippSolovev/HabrStat
$ pip install -r requirements.txt
~~~~

The script uses morphological analyzer 'pymorphy2' to get all the nouns out of article titles. In some cases, a dictionary for the Russian language needs to be installed as a separate package to do this use:

~~~~
$ pip install -U pymorphy2-dicts-ru
~~~~

For additional information about 'pymorphy2' see official documentation (in Russian).

# Built With
* [pymorphy2](https://pymorphy2.readthedocs.io "pymorphy2")
* [pandas](https://pandas.pydata.org "pandas")
* [beautiful soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/ "bs4")
* [requests](http://docs.python-requests.org/en/master/ "requests")

# Authors
* [Filipp Solovev](https://github.com/FilippSolovev "FilippSolovev")

# License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/FilippSolovev/HabrStat/blob/master/LICENSE) file for details
