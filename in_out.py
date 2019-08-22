import csv


def write_csv(file_name, header, rows):
    """
    Write rows represented by a list of dictionaries to a CSV file.

    :param str file_name: name of the file to write to
    :param list[str] header: list of column names
    :param list[dict] rows: rows of the CSV
    """
    with open(file_name, 'r') as outfile:
        writer = csv.DictWriter(outfile, header)
        writer.writeheader()
        writer.writerows(rows)
