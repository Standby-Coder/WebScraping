Stpes to initialize -

1. initialize mariadb and create user "keshav" with password "123456"
2. create database "chewy" and grant all privileges to user "keshav"
3. run init.sh
4. run menu.py
5. Select 1 to run crawler.py to scrap product urls
6. Select 2 to scrap data from product urls collected. 1st output displays the size of the product urls list.
Start scraping from the number in `select count(*) from prod_urls2` and enter an end index to it and assign a batch number to it.

Terminal commands -

sudo mariadb -u root

In mariadb shell -

create user 'keshav'@'localhost' identified by '123456';
create database chewy;
grant all privileges on chewy.* to 'keshav'@'localhost';


Steps to migrate -

1. run migrate.sh

Note -

1. If the url scraped in crawler is not valid, it wait for custom input. Enter the url and press enter. 
2. If you want to skip the url, press enter without entering anything.
3. Batch number in scraper is just for convinience. It helps to keep track of the batch of urls scraped, 
if in case the site goes in maintenance, just run delete on the batch number and start scraping again from the last batch number. 