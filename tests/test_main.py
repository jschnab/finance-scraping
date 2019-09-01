from datetime import datetime
from unittest import TestCase
from unittest.mock import patch, call

from finance_scraping.main import setup, extract, transform, load


class TestMainModule(TestCase):

    def test_setup(self):
        expected = {'bucket': 'bucket', 'profile': 'aws_profile'}
        params = setup('test_log.txt')
        found = {
            'bucket': params['AWS']['s3_bucket'],
            'profile': params['AWS']['profile']
        }
        self.assertEqual(found, expected)

    @patch("finance_scraping.main.ZipFile")
    @patch("finance_scraping.main.BytesIO")
    @patch("finance_scraping.main.logging")
    @patch("finance_scraping.main.aws.upload_object_to_s3")
    @patch("finance_scraping.main.aws.get_s3_key")
    @patch("finance_scraping.main.scraping.get_security_id")
    @patch("finance_scraping.main.scraping.download_page_contents")
    @patch("finance_scraping.main.scraping.get_session")
    @patch("finance_scraping.main.scraping.get_urls")
    def test_extract(
        self,
        get_urls_mock,
        get_session_mock,
        download_page_contents_mock,
        get_security_id_mock,
        get_key_mock,
        upload_object_mock,
        logging_mock,
        bytesio_mock,
        zipfile_mock
    ):
        bytesio_mock = bytesio_mock.return_value
        get_urls_mock.return_value = ['www.myurl.org']
        get_session_mock.return_value = 'session'
        download_page_contents_mock.return_value = 'page contents'
        get_key_mock.return_value = 'archive_key'
        extract(
            'mybucket',
            'key',
            'profile',
            10,
            0.3,
            (500, 502, 504),
            'myownscraper',
            20
        )
        get_urls_mock.assert_called_with('mybucket', 'key', 'profile')
        get_session_mock.assert_called_with(10, 0.3, (500, 502, 504))
        download_page_contents_mock.assert_called_with(
            'session', 'www.myurl.org', 'myownscraper', 20, 10)
        get_security_id_mock.assert_called_with('www.myurl.org')
        get_key_mock.assert_called_with(
            'raw-page-content',
            'archive.zip',
            datetime.today().strftime('%Y/%m/%d')
        )
        upload_object_mock.assert_called_with(
            bytesio_mock,
            'mybucket',
            'archive_key',
            'profile'
        )

    @patch("finance_scraping.main.StringIO")
    @patch("finance_scraping.main.logging")
    @patch("finance_scraping.main.aws.upload_object_to_s3")
    @patch("finance_scraping.main.parsing_html.parse_webpage")
    @patch("finance_scraping.main.ZipFile")
    @patch("finance_scraping.main.BytesIO")
    @patch("finance_scraping.main.aws.download_s3_object")
    @patch("finance_scraping.main.aws.get_s3_key")
    def test_transform(
        self,
        get_key_mock,
        download_object_mock,
        bytesio_mock,
        zipfile_mock,
        parse_webpage_mock,
        upload_object_mock,
        logging_mock,
        stringio_mock
    ):
        stringio_mock = stringio_mock.return_value
        parse_webpage_mock.return_value = {
            'capital': 1982309823,
            'company_name': 'Marshmallows SA'
        }
        zipfile_mock.return_value.namelist.return_value = ['file_name']
        zipfile_mock.return_value.read.return_value.decode.return_value = \
            'webpage contents'
        today_date = datetime.today().strftime('%Y/%m/%d')
        get_key_mock.return_value = 'archive_key'
        transform('mybucket', 'profile')
        get_key_mock.assert_has_calls([
            call('raw-page-content', 'archive.zip', today_date),
            call('parsed-page-data', 'security_report.csv', today_date)
        ])
        download_object_mock.assert_called_with(
            'mybucket',
            'archive_key',
            'profile'
        )
        parse_webpage_mock.assert_called_with('webpage contents', today_date)
        upload_object_mock.assert_called_with(
            stringio_mock,
            'mybucket',
            'archive_key',
            'profile'
        )

    @patch("finance_scraping.main.StringIO")
    @patch("finance_scraping.main.logging")
    @patch("finance_scraping.main.loading.copy_into")
    @patch("finance_scraping.main.utils.remove_header")
    @patch("finance_scraping.main.aws.download_s3_object")
    @patch("finance_scraping.main.aws.get_s3_key")
    @patch("finance_scraping.main.loading.check_table_for_loaded_data")
    @patch("finance_scraping.main.loading.execute_sql_file")
    @patch("finance_scraping.main.loading.get_connection")
    def test_load(
        self,
        connection_mock,
        execute_file_mock,
        check_table_loaded_mock,
        get_key_mock,
        download_object_mock,
        remove_header_mock,
        copy_into_mock,
        logging_mock,
        stringio_mock
    ):
        stringio_mock = stringio_mock.return_value
        download_object_mock.return_value = b'csv data'
        get_key_mock.return_value = 'csv_key'
        today_date = datetime.today().strftime('%Y/%m/%d')
        connection_mock.return_value = 'connection'
        connection_parameters = {
            'database': 'db',
            'username': 'user',
            'password': 'pa$$w0rd',
            'host': 'localhost',
            'port': '1234'
        }
        remove_header_mock.return_value = 'field11,field12\nfield21,field22\n'
        load(connection_parameters, 'mybucket', 'profile')
        connection_mock.assert_has_calls([call(connection_parameters)] * 3)
        execute_file_mock.assert_called_with('create_table.sql', 'connection')
        check_table_loaded_mock.assert_called_with(
            'daily_security_data',
            today_date,
            'connection'
        )
        get_key_mock.assert_called_with(
            'parsed-page-data',
            'security_report.csv',
            today_date
        )
        download_object_mock.assert_called_with(
            'mybucket',
            'csv_key',
            'profile'
        )
        remove_header_mock.assert_called_with('csv data')
        copy_into_mock.assert_called_with(
            file_object=stringio_mock,
            table_name='daily_security_data',
            connection='connection'
        )