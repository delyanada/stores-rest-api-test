import models.store
from tests.unit.unit_base_test import UniteBaseTest


class StoreTest(UniteBaseTest):
    def test_create_store(self):
        store=models.store.StoreModel('test')

        self.assertEqual(store.name, 'test',
                         'The name of the test does not equal the constructor argument')
