import unittest
from stringHelper import StringHelper

class TestStringHelper(unittest.TestCase):
    def setUp(self):
        self.stringHelper = StringHelper()

    def test_IsContainAllWordsInBoardTitle(self):
        keyword = 'apple banana'
        boardTitle = 'I like to eat apple and banana'
        self.assertTrue(self.stringHelper.isWordContainedInParam(keyword, boardTitle))

        keyword = 'apple banana grape'
        boardTitle = 'I like to eat apple and banana'
        self.assertFalse(self.stringHelper.isWordContainedInParam(keyword, boardTitle))
        
    def test_IsContainAnyCommaSeparatedWordsInBoardTitle(self):
        keywords = 'apple, banana, orange'
        boardTitle = 'I like to eat apple and banana'
        self.assertTrue(self.stringHelper.IsContainAnyCommaSeparatedWordsInBoardTitle(keywords, boardTitle))

        keywords = 'grape, peach, plum'
        boardTitle = 'I like to eat apple and banana'
        self.assertFalse(self.stringHelper.IsContainAnyCommaSeparatedWordsInBoardTitle(keywords, boardTitle))

if __name__ == '__main__':
    unittest.main()
