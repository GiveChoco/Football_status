# Football status scraper

In this code, we scrape [https://fbref.com](https://fbref.com), which contains match logs, team and player status of major football leagues. We will be specifically outlining the players abilities on average from both teams and see if there was a hint on who would win or lose. 

# Website used

We used [https://fbref.com](https://fbref.com) because it was accessible using our Beautifulsoup web scraping. Although we tried ESPN, it blocked our request to scrape. 

# How to run this code 

1. Clone the repository 

git clone [https://github.com/GiveChoco/Football\_status](https://github.com/GiveChoco/Football_status)

2. (if necessary) Set up a virtual environment

python \-m venv .venv 

*  On Windows:

.venv\\Scripts\\activate

* On macOS and Linux:

source .venv/bin/activate

3. Install package 

pip install \-r requirements.txt

4. Run the file

python main.py