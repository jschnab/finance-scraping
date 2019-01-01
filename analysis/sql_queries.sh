# run SQLite queries on the database and output results in text files

python3 ~/sqlitetools/sqlitetools/query_db.py -d /home/jonathans/finance-scraping/finance-data.sq3 -q best_ratios.txt

python3 ~/sqlitetools/sqlitetools/query_db.py -d /home/jonathans/finance-scraping/finance-data.sq3 -q best_yields.txt

python3 ~/sqlitetools/sqlitetools/query_db.py -d /home/jonathans/finance-scraping/finance-data.sq3 -q biggest_cies.txt

mv results* output
