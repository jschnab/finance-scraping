top_val_sql = """
    SELECT company_name, {attribute}, date
    FROM security_report_no_nulls
    WHERE date in (SELECT MAX(date) FROM security_report_no_nulls)
    ORDER BY {attribute} DESC
    LIMIT 10;"""

bottom_val_sql = """
    SELECT company_name, {attribute}, date
    FROM security_report_no_nulls
    WHERE date in (SELECT MAX(date) FROM security_report_no_nulls)
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
    ) a
    INNER JOIN security_report_no_nulls B
    ON a.previous_day = b.collection_date AND a.company_name = b.company_name
    ORDER BY diff;"""
