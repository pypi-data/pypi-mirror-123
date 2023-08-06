import unittest

import renxianqi.diff as diff


class DiffTestCase(unittest.TestCase):
    def test_diff(self):
        all_data = """雷学委
        雷小花
        小白
        啊up主
        小Z
        """
        attended_data = """
        雷小花
        小白
        """
        actual = diff.compare(all_data, attended_data)
        exp = ["啊up主", "雷学委", "小Z"]
        self.assertListEqual(exp, actual)


if __name__ == '__main__':
    unittest.main()
