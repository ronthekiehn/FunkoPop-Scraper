# Funko Pop Scraper

A small web scraper for [PopPriceGuide](https://www.poppriceguide.com/) to find the price of a Funko Pop. Also lets you find the prices of high value funko pops that have been autographed. Built with Python using Selenium, re and beautifulsoup. 

## Libraries/Modules Required
* re
* Selenium `pip install selenium`
* bs4 `pip install beautifulsoup4`
* Chrome must be installed

## Usage
`python3 ppg.py`
Prompts will follow.
Can also be reworked to be automatec.

### Inputs (in order)
1. Funko Pop name (ex: Kevin Smith)
2. Reference Number (ex: 37)
    * If not known, then just input nothing and press Enter. It will print out all the listings of the specified Funko Pop.
3. Autographed ("yes" or something else)
    * If "yes", then: Autographer (ex: Kevin Smith)
        * If not known, then just input nothing and press Enter. It will print out all the autographed listings of the specified Funko Pop.
    * If something else, then: no more inputs required

### Process
**If the Funko Pop is not autographed:**
* The web content of the Funko Pop page (in HTML) is loaded
* An HTML parser is used to extract the:
    * Funko Pop Name
    * Reference Number
    * Estimated Value
    * Additional Information (Price on other websites listed on PPG)
* The above pieces of information are printed for every listing available on PPG of the specified Funko Pop

**If the Funko Pop is autographed:**
* The web content of the Funko Pop > Autographed page (in HTML) is loaded
* As there are several listings of any given autographed Funko Pop with different people who have autographed it, the listing(s) with the inputted Autographer is identified
* An HTML parser is used to extract the:
    * Funko Pop Name
    * Reference Number
    * Estimated Value
    * Autographer
    * Additional Information (Price on other websites listed on PPG)
* The above pieces of information are printed for every listing available on PPG of the specified Funko Pop



