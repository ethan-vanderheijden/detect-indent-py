from pathlib import Path
import unittest
import sys

sys.path.append("../src")
from detect_indent import detect_indent


class DetectIndentationTests(unittest.TestCase):
    def test_space_indent(self):
        """detect the indent of a file with space indent"""
        self.assertEqual(
            detect_indent(Path("fixture/space.js").read_text())["indent"], "    "
        )

    def test_space_all(self):
        """return indentation stats for spaces"""
        stats = detect_indent(Path("fixture/space.js").read_text())
        self.assertDictEqual(
            stats,
            {
                "amount": 4,
                "indent": "    ",
                "type": "space",
            },
        )

    def test_tab_four(self):
        """return indentation stats for multiple tabs"""
        stats = detect_indent(Path("fixture/tab-four.js").read_text())
        self.assertDictEqual(
            stats,
            {
                "amount": 4,
                "indent": "\t\t\t\t",
                "type": "tab",
            },
        )

    def test_tab_indent(self):
        """detect the indent of a file with tab indent"""
        self.assertEqual(
            detect_indent(Path("fixture/tab.js").read_text())["indent"], "\t"
        )

    def test_tab_all(self):
        """return indentation stats for tabs"""
        stats = detect_indent(Path("fixture/tab.js").read_text())
        self.assertDictEqual(
            stats,
            {
                "amount": 1,
                "indent": "\t",
                "type": "tab",
            },
        )

    def test_mixed_tab_indent(self):
        """detect the indent of a file with equal tabs and spaces"""
        self.assertEqual(
            detect_indent(Path("fixture/mixed-tab.js").read_text())["indent"], "\t"
        )

    def test_mixed_tab_all(self):
        """return indentation stats for equal tabs and spaces"""
        indent = detect_indent(Path("fixture/mixed-tab.js").read_text())
        self.assertDictEqual(
            indent,
            {
                "amount": 1,
                "indent": "\t",
                "type": "tab",
            },
        )

    def test_mixed_space_indent(self):
        """detect the indent of a file with mostly spaces"""
        stats = detect_indent(Path("fixture/mixed-space.js").read_text())
        self.assertEqual(stats["indent"], "    ")

    def test_mixed_space_all(self):
        """return indentation stats for mostly spaces"""
        stats = detect_indent(Path("fixture/mixed-space.js").read_text())
        self.assertDictEqual(
            stats,
            {
                "amount": 4,
                "indent": "    ",
                "type": "space",
            },
        )

    def test_vendor_prefixed_css_indent(self):
        """detect the indent of a weirdly indented vendor prefixed CSS"""
        stats = detect_indent(Path("fixture/vendor-prefixed-css.css").read_text())
        self.assertEqual(stats["indent"], "    ")

    def test_vendor_prefixed_css_all(self):
        """return indentation stats for various spaces"""
        stats = detect_indent(Path("fixture/vendor-prefixed-css.css").read_text())
        self.assertDictEqual(
            stats,
            {
                "amount": 4,
                "indent": "    ",
                "type": "space",
            },
        )

    def test_no_indentation_amount(self):
        """return `0` when there is no indentation"""
        self.assertEqual(detect_indent("<ul></ul>")["amount"], 0)

    def test_no_indentation_all(self):
        """return indentation stats for no indentation"""
        stats = detect_indent("<ul></ul>")
        self.assertDictEqual(
            stats,
            {
                "amount": 0,
                "indent": "",
                "type": None,
            },
        )

    def test_fifty_fifty_space_first(self):
        """return indentation stats for fifty-fifty indented files with spaces first"""
        stats = detect_indent(Path("fixture/fifty-fifty-space-first.js").read_text())
        self.assertDictEqual(
            stats,
            {
                "amount": 4,
                "indent": "    ",
                "type": "space",
            },
        )

    def test_fifty_fifty_tab_first(self):
        """return indentation stats for fifty-fifty indented files with tabs first"""
        stats = detect_indent(Path("fixture/fifty-fifty-tab-first.js").read_text())
        self.assertDictEqual(
            stats,
            {
                "amount": 1,
                "indent": "	",
                "type": "tab",
            },
        )

    def test_space_tab_last(self):
        """return indentation stats for indented files with spaces and tabs last"""
        stats = detect_indent(Path("fixture/space-tab-last.js").read_text())
        self.assertDictEqual(
            stats,
            {
                "amount": 1,
                "indent": "	",
                "type": "tab",
            },
        )

    def test_single_space_ignore(self):
        """detect the indent of a file with single line comments"""
        stats = detect_indent(Path("fixture/single-space-ignore.js").read_text())
        self.assertDictEqual(
            stats,
            {
                "amount": 4,
                "indent": "    ",
                "type": "space",
            },
        )

    def test_single_space_only(self):
        """return indentations status for indented files with single spaces only"""
        stats = detect_indent(Path("fixture/single-space-only.js").read_text())
        self.assertDictEqual(
            stats,
            {
                "amount": 1,
                "indent": " ",
                "type": "space",
            },
        )

    def test_long_repeat(self):
        """detect the indent of a file with many repeats after a single indent"""
        stats = detect_indent(Path("fixture/long-repeat.js").read_text())
        self.assertEqual(stats["amount"], 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
