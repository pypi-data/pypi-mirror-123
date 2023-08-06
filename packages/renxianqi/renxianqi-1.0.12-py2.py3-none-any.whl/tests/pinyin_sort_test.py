import unittest

import renxianqi.pinyin_sort as ps


class PinyinSortTestCase(unittest.TestCase):
    def test_text2pinyin(self):
        self.assertEqual("lxw", ps.text2pinyin("雷学委"))
        self.assertNotEqual("leixuewei", ps.text2pinyin("雷学委"))

    def test_sort(self):
        input = ["雷学委", "小白", "Abc", "LXW", "LeiXueWei", "Cde", "啊"]
        exp = ['Abc', 'Cde', 'LXW', 'LeiXueWei', '啊', '雷学委', '小白']
        self.assertEqual(exp, sorted(input, key=ps.text2pinyin))
        self.assertNotEqual(exp, ps.sort(input))


if __name__ == '__main__':
    unittest.main()
