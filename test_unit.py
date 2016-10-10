import unittest.mock
import psycopg2
import model
from data_manager import LocalDataManager


class TestAdder(unittest.TestCase):
    def test_create_check(self):
        run = model.Model(LocalDataManager()).create_check('Arnold', 'Schwarzenegger', '0101')
        self.assertTrue(run)

    def test_create_contact(self):
        run = model.Model(LocalDataManager()).create_contact('Arnold', 'Schwarzenegger', '0101')
        res = 'Contact with this phone number is already in Phone Book.'
        self.assertEqual(run, res)

    def test_read(self):
        run = model.Model(LocalDataManager()).read('102')
        res = 'Name: Bruce Willis Phone: 102'
        self.assertEqual(run, res)

    def test_read_all(self):
        run = model.Model(LocalDataManager()).read_all()
        res = 'Name: Bruce Willis Phone: 102'
        self.assertTrue(res in run)

    def test_update_contact(self):
        run = model.Model(LocalDataManager()).update(3, 'Sylvester', 'Stallone', '103')
        res = 'Contact was successfully updated.'
        self.assertEqual(run, res)

    def test_delete_contact(self):
        with self.assertRaises(psycopg2.DataError):
            model.Model(LocalDataManager()).delete('asd')

    def test_select_id(self):
        run = model.Model(LocalDataManager()).select_id('1', 'ID: 1 Name: Bruce Willis Phone: 102')
        res = '1'
        self.assertEqual(run, res)
