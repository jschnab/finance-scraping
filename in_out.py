import csv


def write_csv(file_obj, header, row):
    """
    Write rows represented by a list of dictionaries to a CSV file.

    :param tr file_name: name of the file to write to
    :param list[str] header: list of column names
    :param list[dict] rows: rows of the CSV
    """
    writer = csv.DictWriter(file_obj, header, lineterminator='\n')
    writer.writeheader()
    writer.writerow(row)
