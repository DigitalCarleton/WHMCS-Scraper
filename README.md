# WHMCS Clients Scraper
This project scrapes clients' information from the WHMCS portal and inputs them into a CSV file and an SQLite database.

## Setup
First, clone this repository (```git clone https://github.com/samgjl/WHMCS-Scraper.git```).

You will need the following to run this program:
- A working distribution of Python ([3.11 recommended](https://www.python.org/downloads/release/python-3119/))
- An internet connection
- All packages inside of ```requirements.txt```
<br>(Install Python, then run ```python -m pip install -r requirements.txt```)
- (optional) Install [SQLite](https://sqlite.org/) to work with the ```clients.db``` file.

## Usage
After installing all of the requirements, you can run ```python main.py``` to begin scraping!

### Notes
- If you want to skip entering your username and password, make a document called ```password.txt```. This file should be two (2) lines long: line 1 is your username, and line 2 is your password.
- I have included many utility functions in the ```/helpers/``` folder, but I have not implemented them in the larger web scraper (specifically ```whmcs_overdue.py```). Please tinker with them!