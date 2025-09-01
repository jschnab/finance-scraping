from io import StringIO
from unittest import TestCase
from unittest.mock import patch, call

from finance_scraping.loading import (
    get_connection,
    table_exists,
    execute_sqls,
    execute_sql_file,
    data_already_loaded,
    check_table_for_loaded_data,
    copy_into,
)


class ConnectionMock:
    """
    Class to generate fake psycopg2 database connection objects.
    """
    def __init__(self):
        pass

    def cursor(self):
        return CursorMock()

    def rollback(self):
        pass

    def commit(self):
        pass

    def close(self):
        pass


class CursorMock:
    """
    Class to generate fake psycopg2 cursor objects.
    """
    def __init__(self):
        self.query = None
        self.arguments = None

    def execute(self, query=None, arguments=None):
        self.query = query
        self.arguments = arguments

    def fetchone(self):
        """We return the query passed to the cursor to verify it."""
        return [(self.query, self.arguments)]


class TestLoading(TestCase):

    @patch("finance_scraping.loading.psycopg2.connect")
    def test_get_connection(self, connect_mock):
        connect_mock.return_value = 'engine'
        parameters = {
            'database': 'database',
            'db_user': 'user',
            'password': 'password',
            'host': 'host',
            'port': 'port'
        }
        engine = get_connection(parameters)
        self.assertEqual(engine, 'engine')
        connect_mock.assert_called_with(
            database='database',
            user='user',
            password='password',
            host='host',
            port='port'
        )

    def test_table_exists(self):
        con = ConnectionMock()
        query = """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = %s
        );"""
        result = table_exists('mytable', con)
        self.assertEqual(result, (query, ('mytable',)))

    @patch("finance_scraping.loading.get_connection")
    def test_execute_sqls(self, connection_mock):
        cursor_mock = connection_mock.cursor.return_value
        execute_sqls([("SELECT * FROM mytable;", (42,))], connection_mock)
        connection_mock.cursor.assert_called_once()
        cursor_mock.execute.assert_called_with(
            "SELECT * FROM mytable;", (42,))
        connection_mock.commit.assert_called_once()
        connection_mock.close.assert_called_once()

    @patch("finance_scraping.loading.logging")
    @patch("finance_scraping.loading.get_connection")
    def test_execute_sqls_error(self, connection_mock, logging_mock):
        cursor_mock = connection_mock.cursor.return_value
        cursor_mock.execute.side_effect = ValueError
        with self.assertRaises(ValueError):
            execute_sqls([("SELECT * FROM mytable;", (42,))], connection_mock)
        connection_mock.cursor.assert_called_once()
        logging_mock.critical.assert_called_once()
        connection_mock.rollback.assert_called_once()
        connection_mock.commit.assert_called_once()
        connection_mock.close.assert_called_once()

    @patch("finance_scraping.loading.execute_sqls")
    @patch("finance_scraping.loading.get_connection")
    def test_execute_sql_file(self, connection_mock, execute_mock):
        statements = [
            ('select * from mytable;', ()),
            ('insert into mytable (col1) values (val1);', ())
        ]
        execute_sql_file('test.sql', connection_mock)
        execute_mock.assert_called_with(statements, connection_mock)

    def test_data_already_loaded(self):
        con = ConnectionMock()
        statement = """
        SELECT EXISTS (
            SELECT 1 FROM mytable
            WHERE collection_date = %s
        );"""
        result = data_already_loaded('mytable', '2019-08-31', con)
        self.assertEqual(result, (statement, ('2019-08-31',)))

    @patch("finance_scraping.loading.logging.info")
    @patch("finance_scraping.loading.data_already_loaded")
    @patch("finance_scraping.loading.execute_sqls")
    @patch("finance_scraping.loading.get_connection")
    def test_check_table_for_loaded_data_delete(
        self,
        connection_mock,
        execute_mock,
        loaded_mock,
        logging_mock
    ):
        loaded_mock.return_value = True
        statement = "DELETE FROM %s WHERE collection_date = %s;"
        check_table_for_loaded_data(
            'mytable',
            '2019-08-31',
            connection_mock,
            True
        )
        logging_mock.assert_has_calls([
            call('data was already loaded on 2019-08-31'),
            call("deleting already loaded data from table 'mytable'")
        ])
        execute_mock.assert_called_with(
            [(statement, ('mytable', '2019-08-31'))], connection_mock
        )

    @patch("finance_scraping.loading.logging.info")
    @patch("finance_scraping.loading.data_already_loaded")
    @patch("finance_scraping.loading.get_connection")
    def test_check_table_for_loaded_data_abort(
        self,
        connection_mock,
        loaded_mock,
        logging_mock,
    ):
        loaded_mock.return_value = True
        check_table_for_loaded_data(
            'mytable',
            '2019-08-31',
            connection_mock,
            False
        )
        logging_mock.assert_has_calls([
            call('data was already loaded on 2019-08-31'),
            call("aborting load in table 'mytable'")
        ])

    @patch("finance_scraping.loading.get_connection")
    def test_copy_into(self, connection_mock):
        con = connection_mock.return_value
        cur = con.cursor.return_value
        file_obj = StringIO()
        copy_into(file_obj, 'mytable', con, '|', 'ND')
        cur.copy_from.assert_called_with(
            file=file_obj,
            table='mytable',
            sep='|',
            null='ND'
        )
        con.commit.assert_called_once()
        con.close.assert_called_once()

    @patch("finance_scraping.loading.logging.critical")
    @patch("finance_scraping.loading.get_connection")
    def test_copy_into_error(self, connection_mock, logging_mock):
        con = connection_mock.return_value
        cur = con.cursor.return_value
        cur.copy_from.side_effect = ValueError
        file_obj = StringIO()
        with self.assertRaises(ValueError):
            copy_into(file_obj, 'mytable', con, '|', 'ND')
        cur.copy_from.assert_called_with(
            file=file_obj,
            table='mytable',
            sep='|',
            null='ND'
        )
        logging_mock.assert_called_once()
        con.rollback.assert_called_once()
        con.close.assert_called_once()
