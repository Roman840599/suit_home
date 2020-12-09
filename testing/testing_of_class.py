from class_creator import MyMQTTClass
import unittest


class TestClassCreator(unittest.TestCase):

    def setUp(self):
        self.client = MyMQTTClass('test_client')

    def test_pushing(self):
        self.client.push_message('127.0.0.1', 'thermometer/test_client/temperature', 0, 'Hi')
        self.assertTrue(self.client.has_published)


if __name__ == '__main__':
    unittest.main()
