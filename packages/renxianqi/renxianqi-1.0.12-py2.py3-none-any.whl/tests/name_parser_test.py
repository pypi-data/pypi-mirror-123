import unittest

import renxianqi.name_parser as np


class NameParserTestCase(unittest.TestCase):
    def test_breakdown1(self):
        raw_data = 'Dream丶Killer、宝山的博客、小生凡一'
        actual = np.breakdown(raw_data)
        exp = set(['Dream', 'Killer', '宝山的博客', '小生凡一'])
        self.assertSetEqual(exp, actual)

    def test_breakdown2(self):
        raw_data = """
        Dream丶Killer、宝山的博客、小生凡一
        雷学委
        TestUser，demo，demo
        Test_User
        TestUser
        """
        actual = np.breakdown(raw_data)
        exp = set(['Dream', 'Killer', '宝山的博客', '小生凡一',])
        self.assertNotEquals(exp, actual)

    def test_parse_names_text1(self):
        raw_data = 'Dream丶Killer、宝山的博客、小生凡一'
        actual = np.parse_names_text(raw_data)
        exp = ['Dream', 'Killer', '宝山的博客', '小生凡一']
        self.assertEqual(exp, actual)

    def test_parse_names_text2(self):
        raw_data = """
        Dream丶Killer、宝山的博客、小生凡一
        雷学委
        TestUser，demo，demo
        Test_User
        TestUser
        """
        actual = np.parse_names_text(raw_data)
        exp = ['Dream', 'Killer', 'TestUser', 'Test_User', 'demo', '宝山的博客', '小生凡一', '雷学委']
        self.assertListEqual(exp, actual)


if __name__ == '__main__':
    unittest.main()
