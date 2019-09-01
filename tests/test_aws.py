from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from finance_scraping import aws


@patch("finance_scraping.aws.boto3")
class TestAWS(TestCase):

    def test_get_s3_key(self, boto_mock):
        prefix = 'prefix'
        suffix = 'suffix.ext'
        date = '2019/08/30'
        expected = f'{prefix}/{date}/{suffix}'
        key = aws.get_s3_key(prefix, suffix, date)
        self.assertEqual(key, expected)

    def test_get_client(self, boto_mock):
        session_mock = boto_mock.Session
        client_mock = session_mock.return_value.client
        client_mock.return_value = 'client'
        client = aws.get_client('service', 'profile')
        session_mock.assert_called_with(profile_name='profile')
        client_mock.assert_called_with('service')
        self.assertEqual(client, 'client')

    @patch("finance_scraping.aws.get_client")
    def test_download_s3_object(self, get_client_mock, boto_mock):
        client_mock = get_client_mock.return_value
        response_mock = client_mock.get_object.return_value
        body_mock = response_mock.get.return_value.read
        body_mock.return_value = 'data'
        data = aws.download_s3_object('bucket', 'key', 'profile')
        get_client_mock.assert_called_with('s3', 'profile')
        client_mock.get_object.assert_called_with(Bucket='bucket', Key='key')
        response_mock.get.assert_called_with('Body')
        body_mock.assert_called_once()
        self.assertEqual(data, 'data')

    @patch("finance_scraping.aws.get_client")
    def test_upload_object_to_s3(self, get_client_mock, boto_mock):
        client_mock = get_client_mock.return_value
        put_object_mock = client_mock.put_object
        file_obj = StringIO('text')
        aws.upload_object_to_s3(file_obj, 'bucket', 'key', 'profile')
        get_client_mock.assert_called_with('s3', 'profile')
        put_object_mock.assert_called_with(
            Body='text', Bucket='bucket', Key='key')
