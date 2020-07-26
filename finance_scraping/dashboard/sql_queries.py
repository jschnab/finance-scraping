get_all_data_sql = """SELECT * FROM {}_no_nulls;"""

# need to add 1 day for datepicker to display max date
get_max_date_sql = """
    SELECT TO_CHAR(MAX(collection_date) + INTERVAL '1 DAY', 'YYYY-MM-DD')
    FROM {}_no_nulls;"""

get_min_date_sql = """
    SELECT TO_CHAR(MIN(collection_date), 'YYYY-MM-DD')
    FROM {}_no_nulls;"""

get_companies_sql = """
    SELECT DISTINCT company_name
    FROM {}_no_nulls;"""

top_val_sql = """
    SELECT company_name, {attribute}, date
    FROM security_report_no_nulls
    WHERE date in (SELECT MAX(date) FROM security_report_no_nulls)
    AND {attribute} IS NOT NULL
    ORDER BY {attribute} DESC
    LIMIT 10;"""

bottom_val_sql = """
    SELECT company_name, {attribute}, date
    FROM security_report_no_nulls
    WHERE date in (SELECT MAX(date) FROM security_report_no_nulls)
    AND {attribute} IS NOT NULL
    ORDER BY {attribute}
    LIMIT 10;"""

top_prog_sql = """
    SELECT a.company_name, a.collection_date, a.{attribute} - b.{attribute} AS diff
    FROM (
        SELECT company_name,
            {attribute},
            collection_date,
            LAG(collection_date) OVER (
                PARTITION BY company_name ORDER BY collection_date
            ) AS previous_day
        FROM (
            SELECT *,
                ROW_NUMBER() OVER (
                    PARTITION BY company_name ORDER BY collection_date DESC
                ) AS row
            FROM security_report_no_nulls
        ) b
        WHERE row in (1, 2)
        AND {attribute} IS NOT NULL
    ) a
    INNER JOIN security_report_no_nulls B
    ON a.previous_day = b.collection_date AND a.company_name = b.company_name
    ORDER BY diff DESC;"""

bottom_prog_sql = """
    SELECT a.company_name, a.collection_date, a.{attribute} - b.{attribute} AS diff
    FROM (
        SELECT company_name,
            {attribute},
            collection_date,
            LAG(collection_date) OVER (
                PARTITION BY company_name ORDER BY collection_date
            ) AS previous_day
        FROM (
            SELECT *,
                ROW_NUMBER() OVER (
                    PARTITION BY company_name ORDER BY collection_date DESC
                ) AS row
            FROM security_report_no_nulls
        ) b
        WHERE row in (1, 2)
        AND {attribute} IS NOT NULL
    ) a
    INNER JOIN security_report_no_nulls B
    ON a.previous_day = b.collection_date AND a.company_name = b.company_name
    ORDER BY diff;"""
