CREATE TABLE IF NOT EXISTS daily_security_data (
company_name VARCHAR,
capital FLOAT,
date DATE,
time TIME,
last_quote FLOAT,
last_close FLOAT,
daily_change_abs FLOAT,
daily_change_rel FLOAT,
bid FLOAT,
offer FLOAT,
low FLOAT,
high FLOAT,
day_volume FLOAT,
p_e FLOAT,
yield_percent FLOAT,
collection_date DATE
);
