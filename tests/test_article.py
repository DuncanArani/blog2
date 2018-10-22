import unittest
from app.models import Article

article = Article

class articleTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the blog class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.new_article = article(133,'killed by excelence')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_article,article))
        