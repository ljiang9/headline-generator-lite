"""headline-generator-lite 单元测试。运行：python3 -m unittest discover -s tests"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from generator import (  # noqa: E402
    extract_keywords, generate_rule_based, generate_headlines, generate_with_llm,
)


class TestKeywords(unittest.TestCase):
    def test_extract(self):
        kws = extract_keywords("人工智能 算法 芯片 人工智能 芯片 芯片")
        self.assertEqual(kws[0], "芯片")


class TestRule(unittest.TestCase):
    def test_templates(self):
        hs = generate_rule_based("人工智能 算法 芯片 芯片 算法", n=3)
        self.assertEqual(len(hs), 3)
        self.assertTrue(any("芯片" in h for h in hs))

    def test_empty(self):
        self.assertEqual(generate_rule_based("。。。", n=3), [])


class TestNoKeyFallback(unittest.TestCase):
    def test_no_key_uses_rule(self):
        titles = generate_headlines("人工智能 算法 芯片", n=2)
        self.assertTrue(len(titles) >= 1)
        self.assertEqual(titles[0]["source"], "rule")

    def test_llm_none_without_key(self):
        self.assertIsNone(generate_with_llm("test"))


if __name__ == "__main__":
    unittest.main()
