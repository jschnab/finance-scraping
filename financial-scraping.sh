# script which scrapes financial data from euronext and store data in a sqlite3 database

# scrape the web and put output of python script in variable to check
# if it successfully ran
echo 'Scraping financial data.'
echo 'Please wait, this may take a while...'
check=`python3 scraping.py | tail -c5`

# put data in a sqlite3 database if scraping.py was successful
if [ $check == 'done' ]; then
    echo 'Scraping was successful, now storing data in a database.'
    csvfile=`ls -t *.csv | head -n1`
    python3 ~/sqlitetools/sqlitetools/file2db.py -d ~/finance-scraping/finance-data.sq3 -t euronext_techno -f $csvfile -e latin1

else
    echo 'Scraping was not successful.'
fi
