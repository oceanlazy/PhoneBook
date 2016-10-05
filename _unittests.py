import unittest.mock
import model


class TestAdder(unittest.TestCase):
    def test_add_check(self):
        run = model.Model().add_check('102')
        self.assertTrue(run)

    def test_create_contact(self):
        run = model.Model().create_contact('Foo', 'Bar', '777')
        res = 'Contact successfully created.\nName: Foo Bar Phone: 777'
        self.assertEqual(run, res)

    def test_read(self):
        run = model.Model().read('102')
        res = ['ID - 1 Name: Bruce Willis Phone: 102']
        self.assertEqual(run, res)

    def test_read_all(self):
        run = model.Model().read_all()
        res = ['Name: Arnold Schwarzenegger Phone: 0101', 'Name: Bruce Willis Phone: 102',
               'Name: Sylvester Stallone Phone: 103']
        self.assertEqual(run, res)

    def test_update_contact(self):
        run = model.Model().update_contact(1, 'Foo', 'Bar', '777')
        res = 'Contact successfully updated.\nName: Foo Bar Phone: 777'
        self.assertEqual(run, res)

    def test_delete_contact(self):
        run = model.Model().delete_contact(1)
        res = 'Contact successfully deleted.\nName: Bruce Willis Phone: 102'
        self.assertEqual(run, res)

    def test_select_id(self):
        run = model.Model().select_id('1', ['ID - 1 Name: Bruce Willis Phone: 102'])
        res = '1'
        self.assertEqual(run, res)

    # TODO def test_save_file
