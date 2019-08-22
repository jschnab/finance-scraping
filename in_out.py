import csv


def write_csv(file_obj, header, rows):
    """
    Write rows represented by a list of dictionaries to a CSV file.

    :param tr file_name: name of the file to write to
    :param list[str] header: list of column names
    :param list[dict] rows: rows of the CSV
    """
    writer = csv.DictWriter(outfile, header, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
