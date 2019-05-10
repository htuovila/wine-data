# wine-data

Project parts
1) [x] Scraper
* get product numbers and save to file
* loop through product numbers and request product pages
* parse the product page and save data to dataframe
* save dataframes every 500 products
* finally combine chunks of 500 products into one dataframe
2) [ ] Data Cleaning and feature extraction
* convert string type numerical columns into numerical values
* extract features from name (vintage)
* lists of grapes and characteristics into meaningful features

3) [ ] Data Analytics
* explorative plots on numerical data
* how price changes according to the vintage
* most valuable 
* what else? please let me know if you have any ideas

4) [ ] Make a join to the famous Kaggle wine data set (with reviews)

## Scraper
Makes requests to the www.alko.fi website (or more specifically
to the search page), and compiles a list of product numbers.

Having obtained the product numbers, the scraper moves through
individual product pages, which contain basic product information
in different sections - these can be found using BeautifulSoup to parse
the html.

Running the scraper on a raspberry pi takes approximately 5s per page, and
for this reason I invoked logging to be able to catch possible errors.
So far I have done scraping as an overnight job, and 
